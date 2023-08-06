from __future__ import unicode_literals

from fnmatch import fnmatch
import logging

from .ldap import LDAPError, RDNError, expand_attributes, lower_attributes

from .privilege import Grant
from .privilege import Acl
from .role import (
    Role,
    RoleOptions,
    RoleSet,
)
from .utils import UserError, decode_value, match
from .psql import expandqueries


logger = logging.getLogger(__name__)


class SyncManager(object):
    def __init__(
            self, ldapconn=None, psql=None, inspector=None,
            privileges=None, privilege_aliases=None, blacklist=None,
    ):
        self.ldapconn = ldapconn
        self.psql = psql
        self.inspector = inspector
        self.privileges = privileges or {}
        self.privilege_aliases = privilege_aliases or {}
        self._blacklist = blacklist

    def _query_ldap(self, base, filter, attributes, scope):
        # Query directory returning a list of entries. An entry is a triplet
        # containing Distinguished name, attributes and joins.
        try:
            raw_entries = self.ldapconn.search_s(
                base, scope, filter, attributes,
            )
        except LDAPError as e:
            message = "Failed to query LDAP: %s." % (e,)
            raise UserError(message)

        logger.debug('Got %d entries from LDAP.', len(raw_entries))
        entries = []
        wanted_attribute_names = attributes
        for dn, attributes in raw_entries:
            if not dn:
                logger.debug("Discarding ref: %.40s.", attributes)
                continue

            attributes['dn'] = [dn]
            for n in wanted_attribute_names:
                attributes.setdefault(n, [])

            try:
                entry = decode_value((dn, attributes))
            except UnicodeDecodeError as e:
                message = "Failed to decode data from %r: %s." % (dn, e,)
                raise UserError(message)

            entries.append(lower_attributes(entry) + ({},))

        return entries

    def query_ldap(self, base, filter, attributes, joins, scope):
        logger.info(
            "Querying LDAP %.24s... %.12s...",
            base, filter.replace('\n', ''))
        entries = self._query_ldap(base, filter, attributes, scope)

        join_cache = {}
        for attr, join in joins.items():
            for dn, attrs, entry_joins in entries:
                for value in attrs[attr]:
                    # That would be nice to group all joins of one entry.
                    join_key = '%s/%s' % (attr, value)
                    join_entries = join_cache.get(join_key)
                    if join_entries is None:
                        join_query = dict(join, base=value)
                        try:
                            logger.info("Sub-querying LDAP %.24s...", value)
                            join_entries = self._query_ldap(**join_query)
                            join_cache[join_key] = join_entries
                        except UserError as e:
                            logger.warning('Ignoring %s: %s', value, e)
                            join_cache[join_key] = False
                            continue
                    if join_entries:
                        join_entries += entry_joins.get(attr, [])
                        entry_joins[attr] = join_entries

        return entries

    def process_ldap_entry(self, entry, names, **kw):
        members = list(expand_attributes(entry, kw.get('members', [])))
        parents = list(expand_attributes(entry, kw.get('parents', [])))
        comment = kw.get('comment', None)
        if comment:
            try:
                comment = next(expand_attributes(entry, [comment]))
            except StopIteration:
                logger.warning(
                    "Can't generate comment for %s... Missing attribute?",
                    entry[0][:24])
                comment = None

        for name in expand_attributes(entry, names):
            log_source = " from " + ("YAML" if name in names else entry[0])

            logger.debug("Found role %s%s.", name, log_source)
            if members:
                logger.debug(
                    "Role %s must have members %s.", name, ', '.join(members),
                )
            if parents:
                logger.debug(
                    "Role %s is member of %s.", name, ', '.join(parents))
            role = Role(
                name=name,
                members=members[:],
                options=kw.get('options', {}),
                parents=parents[:],
                comment=comment,
            )

            yield role

    def apply_role_rules(self, rules, entries):
        for rule in rules:
            on_unexpected_dn = rule.get('on_unexpected_dn', 'fail')
            for entry in entries:
                try:
                    for role in self.process_ldap_entry(entry=entry, **rule):
                        yield role
                except RDNError as e:
                    msg = "Unexpected DN: %s" % e.dn
                    if 'ignore' == on_unexpected_dn:
                        continue
                    elif 'warn' == on_unexpected_dn:
                        logger.warning(msg)
                    else:
                        raise UserError(msg)
                except ValueError as e:
                    msg = "Failed to process %.48s: %s" % (entry[0], e,)
                    raise UserError(msg)

    def apply_grant_rules(self, grant, entries=[]):
        for rule in grant:
            privilege = rule.get('privilege')

            databases = rule.get('databases', '__all__')
            if databases == '__all__':
                databases = Grant.ALL_DATABASES

            schemas = rule.get('schemas', '__all__')
            if schemas in (None, '__all__', '__any__'):
                schemas = None

            pattern = rule.get('role_match')

            for entry in entries:
                try:
                    roles = list(expand_attributes(entry, rule['roles']))
                except ValueError as e:
                    msg = "Failed to process %.32s: %s" % (entry, e,)
                    raise UserError(msg)

                for role in roles:
                    role = role.lower()
                    if pattern and not fnmatch(role, pattern):
                        logger.debug(
                            "Don't grant %s to %s not matching %s.",
                            privilege, role, pattern,
                        )
                        continue
                    yield Grant(privilege, databases, schemas, role)

    def inspect_ldap(self, syncmap):
        ldaproles = {}
        ldapacl = Acl()
        for mapping in syncmap:
            if 'ldap' in mapping:
                entries = self.query_ldap(**mapping['ldap'])
                log_source = 'in LDAP'
            else:
                entries = [None]
                log_source = 'from YAML'

            for role in self.apply_role_rules(mapping['roles'], entries):
                if role in ldaproles:
                    try:
                        role.merge(ldaproles[role])
                    except ValueError:
                        msg = "Role %s redefined with different options." % (
                            role,)
                        raise UserError(msg)
                ldaproles[role] = role

            grant = mapping.get('grant', [])
            grants = self.apply_grant_rules(grant, entries)
            for grant in grants:
                logger.debug("Found GRANT %s %s.", grant, log_source)
                ldapacl.add(grant)

        # Lazy apply of role options defaults
        roleset = RoleSet()
        for role in ldaproles.values():
            role.options.fill_with_defaults()
            roleset.add(role)

        return roleset, ldapacl

    def postprocess_acl(self, acl, schemas):
        expanded_grants = acl.expandgrants(
            aliases=self.privilege_aliases,
            privileges=self.privileges,
            databases=schemas,
        )

        acl = Acl()
        try:
            for grant in expanded_grants:
                acl.add(grant)
        except ValueError as e:
            raise UserError(e)

        return acl

    def sync(self, syncmap):
        logger.info("Inspecting roles in Postgres cluster...")
        me, issuper = self.inspector.fetch_me()
        if not match(me, self.inspector.roles_blacklist):
            self.inspector.roles_blacklist.append(me)

        if not issuper:
            logger.warning("Running ldap2pg as non superuser.")
            RoleOptions.filter_super_columns()

        databases, pgallroles, pgmanagedroles = self.inspector.fetch_roles()
        pgallroles, pgmanagedroles = self.inspector.filter_roles(
            pgallroles, pgmanagedroles)

        logger.debug("Postgres roles inspection done.")
        ldaproles, ldapacl = self.inspect_ldap(syncmap)
        logger.debug("LDAP inspection completed. Post processing.")
        try:
            ldaproles.resolve_membership()
        except ValueError as e:
            raise UserError(str(e))

        count = 0
        count += self.psql.run_queries(expandqueries(
            pgmanagedroles.diff(other=ldaproles, available=pgallroles),
            databases=databases))
        if self.privileges:
            logger.info("Inspecting GRANTs in Postgres cluster...")
            # Inject ldaproles in managed roles to avoid requerying roles.
            pgmanagedroles.update(ldaproles)
            if self.psql.dry and count:
                logger.warning(
                    "In dry mode, some owners aren't created, "
                    "their default privileges can't be determined.")
            schemas = self.inspector.fetch_schemas(databases, ldaproles)
            pgacl = self.inspector.fetch_grants(schemas, pgmanagedroles)
            ldapacl = self.postprocess_acl(ldapacl, schemas)
            count += self.psql.run_queries(expandqueries(
                pgacl.diff(ldapacl, self.privileges),
                databases=schemas))
        else:
            logger.debug("No privileges defined. Skipping GRANT and REVOKE.")

        if count:
            # If log does not fit in 24 row screen, we should tell how much is
            # to be done.
            level = logger.debug if count < 20 else logger.info
            level("Generated %d querie(s).", count)
        else:
            logger.info("Nothing to do.")

        return count
