docker build -t nuodb:latest .<br>
docker run -d -p 48004:48004 -p 48005:48005 -p 48006:48006 -p 8888:8888 -p 9001:9001 nuodb:latest<br>
service nuoagent start<br>
service nuorestsvc start<br>
bin/nuodbmgr --broker localhost --password bird<br>
https://github.com/yrobla/docker-nuodb/blob/master/Dockerfile<br>


https://download.nuohub.org/ce_releases/nuodb-ce_4.0.1.1_amd64.deb?Expires=1569536890&Signature=Fj2v6ofXpCIk74w3op1tIBD5OeepvLr55iWMxZnFXQoevXSH4ka1dA0RKCMa6yhVx5CPUhMQfGc3GwX~gcHrbxOUI6isqipjCyEOc35W3o5NNe9JRLhs-HQ23yx0hk8tQ8eAggDXnI2A5PT30cvTdY8oLctXFtoI22U8pKkNbcaQI34U3DKvjywymytXn2cT14A31M42XCaM~~YcGp5fisYgfGzYbeiGa7LyXJd9DhVe566msO~7ZDUuR8QrUM5qnTRVSOZgHltJbsmKv5oBfOp-B3yqRT4YgHViuWAvbveMrI8zgocRQv167CmnLgZbAOQVr2DrcolvDrGnOSXa6A__&Key-Pair-Id=APKAJCMYGOXC7TLH2MKA
