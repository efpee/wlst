def getJMSModulePath(jmsModuleName):
    return "/JMSSystemResources/" + jmsModuleName + "/JMSResource/" + jmsModuleName

def createJMSServer(jmsServerName, managedServer):
  print "Creating JMS Server " + jmsServerName + " targetted to " + managedServer
  cd('/JMSServers')
  jmsServer = cmo.lookupJMSServer(jmsServerName)
  if jmsServer == None:
    jmsServer = create(jmsServerName, 'JMSServer')
    #jmsServer.setMessagesMaximum(20000)
    #jmsServer.setBytesMaximum(200000000)
    target = getMBean('/Servers/' + managedServer)
    jmsServer.addTarget(target)
    fileStore = create(jmsServerName + '-FileStore', 'FileStore')
    fileStore.setDirectory(DOMAIN_DIR + 'FileStore-' + jmsServerName)
    fileStore.addTarget(target)
    jmsServer.setPersistentStore(fileStore)
  else:
    print "JMS Server with name '" + jmsServerName + "' already exists"
    print "Skipping configuration"
  return jmsServer
  
# targetName can be either a ManagedServer or a Cluster
def createJMSModule(jmsModuleName, subDeploymentName, targetName, jmsServers):
  print "Creating JMS Module " + jmsModuleName
  cd('/JMSSystemResources')
  jmsSystemResource = cmo.lookupJMSSystemResource(jmsModuleName)
  if jmsSystemResource == None:
    jmsSystemResource = create(jmsModuleName, 'JMSSystemResource')
    jmsSystemResource.addTarget(getMBean(targetName))
    createSubDeployment(subDeploymentName, jmsSystemResource, targetName, jmsServers)
  else:
    print "JMS Module: '" + jmsModuleName + "' already exists"
    print "Skipping configuration"
  return jmsSystemResource

def createSubDeployment(subDeploymentName, jmsSystemResource, target, jmsServers):
  print "Creating subdeployment " + subDeploymentName
  subDep = jmsSystemResource.createSubDeployment(subDeploymentName)
  if len(jmsServers) == 0:
    subDep.addTarget(getMBean(target))
  else:
    for jmsServer in jmsServers:
      subDep.addTarget(jmsServer)
  return subDep
  
# create JMS connection factory
def createConnectionFactory(jmsResource, cFactoryName, cFactoryJNDI, xaEnabled, subDeploymentName):
  print 'Creating connection factory: ' + cFactoryName
  myConnectionFactory = jmsResource.lookupConnectionFactory(cFactoryName)
  if myConnectionFactory == None:
    myConnectionFactory = jmsResource.createConnectionFactory(cFactoryName)
    myConnectionFactory.setJNDIName(cFactoryJNDI)
    myConnectionFactory.getTransactionParams().setXAConnectionFactoryEnabled(xaEnabled)
    myConnectionFactory.setSubDeploymentName(subDeploymentName)
    
def createUniformDistributedQueue(jmsResource, queueName, queueJNDI, subDeploymentName, timeToLive=-1, forwardDelay=-1):
  print 'Creating uniform distributed queue: ' + queueName
  jmsQueue = jmsResource.lookupUniformDistributedQueue(queueName)
  if jmsQueue == None:
    jmsQueue = jmsResource.createUniformDistributedQueue(queueName)
    jmsQueue.setJNDIName(queueJNDI)
    jmsQueue.setSubDeploymentName(subDeploymentName)
    jmsQueue.setLoadBalancingPolicy('Round-Robin')
    jmsQueue.setResetDeliveryCountOnForward(true)
    jmsQueue.setForwardDelay(forwardDelay)
    jmsQueue.getDeliveryParamsOverrides().setTimeToLive(timeToLive)
  return jmsQueue

def configUniformDistributedQueueErrorHandling(queueName, errorQueueName, redeliveries):
  print "Setting error queue for " + queueName + " to " + errorQueueName
  queue = jmsResource.lookupUniformDistributedQueue(queueName)
  if errorQueueName:
    errorQueue = jmsResource.lookupUniformDistributedQueue(errorQueueName)
    queue.getDeliveryFailureParams().setErrorDestination(errorQueue)
    queue.getDeliveryFailureParams().setExpirationPolicy('Redirect');
  queue.getDeliveryParamsOverrides().setRedeliveryDelay(1000)
  queue.getDeliveryFailureParams().setRedeliveryLimit(redeliveries)
             
def createForeignJMSServer(serverName, moduleName, subDeploymentName, url):
  try:
    print 'Creating foreign JMS Server: ' + serverName
    cd(getJMSModulePath(moduleName))
    foreignServer = cmo.createForeignServer(serverName)
    foreignServer.setConnectionURL(url)
    foreignServer.setSubDeploymentName(subDeploymentName)
    foreignServer.setJNDIPropertiesCredentialEncrypted(encrypt(password, DOMAIN_DIR))
    prop = foreignServer.createJNDIProperty('java.naming.security.principal')
    prop.setValue(username)
    return foreignServer
  except weblogic.descriptor.BeanAlreadyExistsException:
    print "ForeignJMSServer '" + serverName + "' already exists"
    print "Will skip ForeignJMSServer configuration except for destination creation"
    cd(getJMSModulePath(moduleName) + '/ForeignServers')
    return cmo.lookupForeignServer(serverName)
          
def createForeignDestination(foreignServer, name, local_jndi, remote_jndi):
  try:
    print "Creating foreign destination '" + name + "'"
    dest = foreignServer.createForeignDestination(name)
    dest.setLocalJNDIName(local_jndi)
    dest.setRemoteJNDIName(remote_jndi)
    return dest
  except weblogic.descriptor.BeanAlreadyExistsException:
    print "Foreign destination with name '" + name + "' already exists"
    print "Configuration was skipped"
    return foreignServer.lookupForeignDestination(name)
         
def createForeignConnectionFactory(foreignServer, name, local_jndi, remote_jndi):
  try:
    print "Creating foreign ConnectionFactory '" + name + "'"
    cf = foreignServer.createForeignConnectionFactory(name)
    cf.setLocalJNDIName(local_jndi)
    cf.setRemoteJNDIName(remote_jndi)
    return cf
  except weblogic.descriptor.BeanAlreadyExistsException:
    print "The foreign ConnectionFactory with name '" + name + "' already exists"
    print "Configuration skipped"
    return foreignServer.lookupForeignConnectionFactory(name)

