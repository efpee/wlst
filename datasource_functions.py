def createJDBCDataSource(name, jndi, target, driverClass, url, username, password, initialCapacity=1, minCapacity=1, maxCapacity=5):
  cd('/')
  jdbcSysRes = cmo.lookupJDBCSystemResource(name) 
  if jdbcSysRes is None:
    jdbcSysRes = cmo.createJDBCSystemResource(name)
    jdbcRes = jdbcSysRes.getJDBCResource()
    jdbcRes.setName(name)
    dataSourceParms = jdbcRes.getJDBCDataSourceParams()
    dataSourceParams.addJNDIName(jndi)
    driverParams = jdbcRes.getJDBCDriverParams()  
    driverParams.setUrl(url)
    driverParams.setDriverName(driverClass)
    driverParams.setPassword(password)
    connPoolParams = jdbcRes.getJDBCConnectionPoolParams()
    connPoolParams.setTestTableName('select * from dual')
    connPoolParams.setInitialCapacity(initialCapacity)
    connPoolParams.setMaxCapacity(minCapacity)    
    connPoolParams.setMinCapacity(maxCapacity)
    props = driverParams.getProperties()
    userProp = props.createProperty('user')
    userProp.setValue(username)
    jdbcSysRes.addTarget(target)
  else:
    print ' - jdbc system resource ' + name + ' already exists and will not be configured.'

