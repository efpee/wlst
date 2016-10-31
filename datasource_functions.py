def createJDBCDataSource(name, jndi, targets, driverClass, url, username, password):
  cd('/')
  jdbcSysRes = cmo.lookupJDBCSystemResource(name) 
  if jdbcSysRes is None:
    print ' - Creating jdbc system resource ' + name + '.'
    jdbcSysRes = cmo.createJDBCSystemResource(name)
    jdbcRes = jdbcSysRes.getJDBCResource()
    jdbcRes.setName(name)
    dataSourceParams = jdbcRes.getJDBCDataSourceParams()
    dataSourceParams.addJNDIName(jndi)
    driverParams = jdbcRes.getJDBCDriverParams()  
    driverParams.setUrl(url)
    driverParams.setDriverName(driverClass)
    driverParams.setPassword(password)
    props = driverParams.getProperties()
    userProp = props.createProperty('user')
    userProp.setValue(username)
    for target in targets:
      if not target is None:
        jdbcSysRes.addTarget(target)
      else:
        print ' -- Could not set target.'
    return jdbcRes
  else:
    print ' - jdbc system resource ' + name + ' already exists and will not be configured.'
    return None

def configureConnectionPool(jdbcRes, initialCapacity=1, minCapacity=1, maxCapacity=5, secondsToTrustAnIdlePoolConnection=0, connectionCreationRetryFrequencySeconds=10):
  if not jdbcRes is None:
    print '-- Configuring connection pool for ' + jdbcRes.getName()
    connPoolParams = jdbcRes.getJDBCConnectionPoolParams()
    connPoolParams.setTestTableName('select * from dual')
    connPoolParams.setInitialCapacity(initialCapacity)
    connPoolParams.setMinCapacity(minCapacity)    
    connPoolParams.setMaxCapacity(maxCapacity)
    connPoolParams.setSecondsToTrustAnIdlePoolConnection(secondsToTrustAnIdlePoolConnection)
    connPoolParams.setConnectionCreationRetryFrequencySeconds(connectionCreationRetryFrequencySeconds)

  else:  
    print '-- Warning: No jdbc resource to configure connection pool settings'   
 
def configureGridLinkDataSource(jdbcRes, nodeList, fanEnabled = true):
  if not jdbcRes is None:
    print '-- Configuring grid link data source for ' + jdbcRes.getName()
    oracleJdbcParams = jdbcRes.getJDBCOracleParams()
    nodes = ','.join(nodeList)
    oracleJdbcParams.setOnsNodeList(nodes)
    oracleJdbcParams.setFanEnabled(fanEnabled)
  else:
    print '-- Warning: No jdbc resource to configure grid link settings'  
