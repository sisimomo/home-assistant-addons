import json
import os
import itertools

def cloudflareOptionStructureToConfigStructure(cloudflareItem):
  return {
    "authentication": optionStructureToConfigAuthenticationStructure(cloudflareItem),
    "zone_id": cloudflareItem["zone_id"],
    "subdomains": [
      {
        "name": cloudflareItem["subdomains_name"],
        "proxied": cloudflareItem["subdomains_proxied"]
      }
    ]
  }

def loadBalancerOptionStructureToConfigStructure(loadBalancerItem):
  return {
    "authentication": optionStructureToConfigAuthenticationStructure(loadBalancerItem),
    "pool_id": loadBalancerItem["pool_id"],
    "origin": loadBalancerItem["origin"]
  }

def optionStructureToConfigAuthenticationStructure(item):
  if "authentication_api_token" in item:
    return {
      "api_token": item["authentication_api_token"]
    }
  elif "authentication_api_key" in item and "authentication_account_email" in item:
    return {
      "api_key": {
        "api_key": item["authentication_api_key"],
        "account_email": item["authentication_account_email"]
      }
    }

def optimizeCloudflareItems(cloudflareItems):
  optimizedCloudflareItems = []
  for cloudflareItem in cloudflareItems:
    alreadyTreated = len(list(filter(lambda x: cloudflareItemSimilar(x, cloudflareItem), optimizedCloudflareItems))) > 0
    if not optimizedCloudflareItems or not alreadyTreated:
      similar = list(filter(lambda x: cloudflareItemSimilar(x, cloudflareItem), cloudflareItems))
      newItem = json.loads(json.dumps(cloudflareItem)) #clone
      newItem["subdomains"] = list(itertools.chain.from_iterable(map(lambda x: (x["subdomains"]), similar)))
      optimizedCloudflareItems.append(newItem)
  return optimizedCloudflareItems

def cloudflareItemSimilar(a, b):
  return a["authentication"] == b["authentication"] and a["zone_id"] == b["zone_id"]


CONFIG_PATH = os.environ.get('CONFIG_PATH', os.getcwd())

options = None
try:
  with open(os.path.join(CONFIG_PATH, "options.json")) as options_file:
      options = json.loads(options_file.read())
except:
  print("😡 Error reading options.json")

if options is not None:
  config = {
    "cloudflare": optimizeCloudflareItems(list(map(cloudflareOptionStructureToConfigStructure, options["cloudflare"]))),
    "load_balancer": list(map(loadBalancerOptionStructureToConfigStructure, options["load_balancer"])),
    "a": options["a"],
    "aaaa": options["aaaa"],
    "purgeUnknownRecords": options["purgeUnknownRecords"],
    "ttl": options["ttl"]
  }

  try:
    with open(os.path.join(CONFIG_PATH, "config.json"), "w") as outfile:
      outfile.write(json.dumps(config))
  except:
    print("😡 Error writing config.json")

else:
  print("😡 Error reading options.json")