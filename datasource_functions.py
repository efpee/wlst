def createJDBCDataSource(name, jndi, targets, driverClass, url, username, password, initialCapacity=1, minCapacity=1, maxCapacity=5):
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
    connPoolParams = jdbcRes.getJDBCConnectionPoolParams()
    connPoolParams.setTestTableName('select * from dual')
    connPoolParams.setInitialCapacity(initialCapacity)
    connPoolParams.setMinCapacity(minCapacity)    
    connPoolParams.setMaxCapacity(maxCapacity)
    props = driverParams.getProperties()
    userProp = props.createProperty('user')
    userProp.setValue(username)
    for target in targets:
      if not target is None:
        jdbcSysRes.addTarget(target)
      else:
        print ' -- Could not set target.'
  else:
    print ' - jdbc system resource ' + name + ' already exists and will not be configured.'

