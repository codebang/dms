invoke sample:
   from dmsinventory.inventory import DMSInventory
   
   inventory = DMSInventory()
   
   inventory.getnamebyaid(accountid)
  
   inventory.getusrbyip(accountid,usr)


For the beheavior:
   first check the cache , if cache missing , retrieve from zookeeper.
   at the same time, add the watcher for the corresponding node , then the node will exist in cache and update by watcher.
   if can not get the node finally , will return None



   
