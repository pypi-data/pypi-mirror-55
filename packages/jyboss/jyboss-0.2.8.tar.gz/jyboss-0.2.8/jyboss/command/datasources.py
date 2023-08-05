# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)

from jyboss.exceptions import ParameterError, NotFoundError
from jyboss.command.core import BaseJBossModule
from jyboss.logging import debug

__metaclass__ = type

try:
    dict.iteritems
except AttributeError:
    # Python 3
    def iteritems(d):
        return d.items()
else:
    # Python 2
    def iteritems(d):
        return d.iteritems()


class DatasourcesModule(BaseJBossModule):
    SUBSYSTEM_PARAMS = [
        'data-source',
        'xa-data-source',
        'jdbc-driver'
    ]

    DATASOURCE_PARAMS = [
        'allocation-retry',
        'allocation-retry-wait-millis',
        'allow-multiple-users',
        'background-validation',
        'background-validation-millis',
        'blocking-timeout-wait-millis',
        'capacity-decrementer-class',
        'capacity-decrementer-properties',
        'capacity-incrementer-class',
        'capacity-incrementer-properties',
        'check-valid-connection-sql',
        'connectable',
        'connection-listener-class',
        'connection-listener-property',
        'connection-url',
        'datasource-class',
        'driver-class',
        'driver-name',
        'enabled',
        'enlistment-trace',
        'exception-sorter-class-name',
        'exception-sorter-properties',
        'flush-strategy',
        'idle-timeout-minutes',
        'initial-pool-size',
        'interleaving',
        'jndi-name',
        'jta',
        'max-pool-size',
        'mcp',
        'min-pool-size',
        'new-connection-sql',
        'no-recovery',
        'no-tx-separate-pool',
        'pad-xid',
        'password',
        'pool-fair',
        'pool-name',  # looks like cli scripting api will use the name of the data source as pool name and ignores this
        'pool-prefill',
        'pool-use-strict-min',
        'prepared-statements-cache-size',
        'query-timeout',
        'reauth-plugin-class-name',
        'reauth-plugin-properties',
        'recovery-password',
        'recovery-plugin-class-name',
        'recovery-plugin-properties',
        'recovery-security-domain',
        'recovery-username',
        'same-rm-override',
        'security-domain',
        'set-tx-query-timeout',
        'share-prepared-statements',
        'spy',
        'stale-connection-checker-class-name',
        'stale-connection-checker-properties',
        'statistics-enabled',
        'tracking',
        'track-statements',
        'transaction-isolation',
        'url-delimiter',
        'url-selector-strategy-class-name',
        'use-ccm',
        'use-fast-fail',
        'use-java-context',
        'user-name',
        'use-try-lock',
        'validate-on-match',
        'valid-connection-checker-class-name',
        'valid-connection-checker-properties',
        'wrap-xa-resource',
        'xa-datasource-class',
        'xa-resource-timeout'
    ]

    DATASOURCE_NON_UPDATEABLE_PARAMS = [
        'jta',
        'pool-name'
    ]

    JDBC_DRIVER_PARAMS = [
        'deployment-name',
        'driver-class-name',
        'driver-datasource-class-name',
        'driver-major-version',
        'driver-minor-version',
        'driver-module-name',
        'driver-name',
        'driver-xa-datasource-class-name',
        'module-slot',
        'profile',
        'xa-datasource-class'
    ]

    JDBC_DRIVER_NON_UPDATEABLE_PARAMS = [
        'deployment-name',
        'driver-class-name',
        'driver-datasource-class-name',
        'driver-xa-datasource-class-name',
        'driver-major-version',
        'driver-minor-version',
        'driver-module-name',
        'driver-name',
        'module-slot',
        'profile',
        'xa-datasource-class'
    ]

    def __init__(self, context=None):
        super(DatasourcesModule, self).__init__(path='/subsystem=datasources', context=context)

    def apply(self, datasources=None, **kwargs):

        datasources = self.unescape_keys(datasources)

        if not isinstance(datasources, dict):
            raise ParameterError('%s provided to %s is not an allowable type' % (datasources, self.__class__.__name__))

        changes = []

        for key in datasources.keys():

            if key in ['data-source', 'xa-data-source']:
                ds = self._format_apply_param(datasources[key])
                changes += self.apply_datasources(ds, key)
            elif key == 'jdbc-driver':
                drivers = self._format_apply_param(datasources[key])
                changes += self.apply_jdbc_drivers(drivers)
            else:
                debug('%s.apply(): Unrecognised property %s => %r' % (self.__class__.__name__, key, datasources[key]))

        return changes if len(changes) > 0 else None

    def apply_datasources(self, datasources, datasource_type):

        changes = []
        for ds in datasources:

            name = self._get_param(ds, 'name')

            state = self._get_param(ds, 'state')

            if state not in ['present', 'absent']:
                raise ParameterError('The datasource state is not one of [present|absent]')

            if state == 'present':
                changes += self.apply_datasource_present(name, datasource_type, ds)
            elif state == 'absent':
                changes += self.apply_datasource_absent(name, datasource_type)

        return changes

    def apply_datasource_absent(self, name, datasource_type):

        try:
            self.cmd('%s/%s=%s:remove()' % (self.path, datasource_type, name))
            return [{'datasource': name, 'type': datasource_type, 'action': 'delete'}]
        except NotFoundError:
            return []

    def apply_datasource_present(self, name, datasource_type, datasource):

        ds_path = '%s/%s=%s' % (self.path, datasource_type, name)

        changes = []
        try:
            ds_dmr = self.read_resource_dmr(ds_path)
            # update datasource
            fc = dict((k, v) for (k, v) in iteritems(datasource) if
                      k in self.DATASOURCE_PARAMS and k not in self.DATASOURCE_NON_UPDATEABLE_PARAMS)

            a_changes = self._sync_attributes(parent_node=ds_dmr,
                                              parent_path=ds_path,
                                              target_state=fc,
                                              allowable_attributes=self.DATASOURCE_PARAMS)

            # also sync existing xa props
            if 'xa-datasource-properties' in datasource:
                a_changes += self.apply_xa_properties(datasource_type, name, datasource['xa-datasource-properties'])

            if len(a_changes) > 0:
                changes.append({'datasource': name, 'type': datasource_type, 'action': 'update', 'changes': a_changes})

        except NotFoundError:
            # create the datasource
            ds_params = self.convert_to_dmr_params(datasource, self.DATASOURCE_PARAMS)
            self.cmd('%s/%s=%s:add(%s)' % (self.path, datasource_type, name, ds_params))

            add_change = {
                'datasource': name,
                'type': datasource_type,
                'action': 'add',
                'params': ds_params
            }

            if 'xa-datasource-properties' in datasource:
                xa_params = self.apply_xa_properties(datasource_type, name, datasource['xa-datasource-properties'])
                add_change['xa-datasource-properties'] = xa_params

            changes.append(add_change)

        return changes

    def apply_xa_properties(self, datasource_type, name, properties):

        changes = []

        for key, new_value in iteritems(properties):
            ds_path = '%s/%s=%s/xa-datasource-properties=%s' % (self.path, datasource_type, name, key)
            # test if value exists
            try:
                dmr = self.read_attribute_dmr(ds_path, 'value')
                old_value = self.dmr_to_python(dmr)
                if new_value is None:  # if value is none, remove it
                    self.cmd('%s:remove()' % ds_path)
                    changes.append({'attribute': key, 'action': 'delete', 'old_value': old_value})
                elif new_value is not None and new_value != old_value:  # if value is not none, add or update it
                    self.cmd('%s:remove()' % ds_path)
                    self.cmd('%s:add(value=%s' % (ds_path, self.convert_type(new_value)))
                    changes.append({
                        'attribute': key,
                        'action': 'update',
                        'old_value': old_value,
                        'new_value': new_value
                    })
            except NotFoundError:
                if new_value is not None:  # if value is not none, add it
                    self.cmd('%s:add(value=%s' % (ds_path, self.convert_type(new_value)))
                    changes.append({'attribute': key, 'action': 'add', 'new_value': new_value})

        return changes

    # JDBC Driver
    def apply_jdbc_drivers(self, jdbc_drivers):

        changes = []
        for jdbc_driver in jdbc_drivers:

            name = self._get_param(jdbc_driver, 'name')

            state = self._get_param(jdbc_driver, 'state')

            if state not in ['present', 'absent']:
                raise ParameterError('The jdbc driver state is not one of [present|absent]')

            if state == 'present':
                changes += self.apply_jdbc_driver_present(name, jdbc_driver)
            elif state == 'absent':
                changes += self.apply_jdbc_driver_absent(name)

        return changes

    def apply_jdbc_driver_absent(self, name):

        try:
            self.cmd('%s/jdbc-driver=%s:remove()' % (self.path, name))
            return [{'jdbc-driver': name, 'action': 'delete'}]
        except NotFoundError:
            return []

    def apply_jdbc_driver_present(self, name, jdbc_driver):

        jdbc_driver_path = '%s/jdbc-driver=%s' % (self.path, name)

        changes = []
        try:
            jdbc_driver_dmr = self.read_resource_dmr(jdbc_driver_path)
            # update jdbc_driver
            for (k, v) in iteritems(jdbc_driver):
                if k in self.JDBC_DRIVER_NON_UPDATEABLE_PARAMS:
                    debug('Warning, parameter %s cannot be updated on jdbc driver and will be ignored' % k)

            fc = dict(
                (k, v) for (k, v) in iteritems(jdbc_driver) if
                k in self.JDBC_DRIVER_PARAMS and k not in self.JDBC_DRIVER_NON_UPDATEABLE_PARAMS)
            a_changes = self._sync_attributes(parent_node=jdbc_driver_dmr,
                                              parent_path=jdbc_driver_path,
                                              target_state=fc,
                                              allowable_attributes=self.JDBC_DRIVER_PARAMS)
            if len(a_changes) > 0:
                changes.append({'jdbc-driver': name, 'action': 'update', 'changes': a_changes})

        except NotFoundError:
            # little hack to maintain sanity, for some reason one has to supply the name of the driver in the list of
            # parameters again, the param itself appears to be thrown away however
            if 'driver-name' not in jdbc_driver:
                jdbc_driver['driver-name'] = name

            jdbc_driver_params = self.convert_to_dmr_params(jdbc_driver, self.JDBC_DRIVER_PARAMS)
            self.cmd('%s/jdbc-driver=%s:add(%s)' % (self.path, name, jdbc_driver_params))
            changes.append({'jdbc-driver': name, 'action': 'add', 'params': jdbc_driver_params})

        return changes
