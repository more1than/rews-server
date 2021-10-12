from pkg.cloud_provider.ctyun.disk.disk import Disk
from pkg.cloud_provider.ctyun.image.image import Image
from pkg.cloud_provider.ctyun.node.node import Node
from pkg.cloud_provider.ctyun.network.network import Network


class Ctyun():
    def __init__(self, name, access_key, security_key):
        self.AccessKey = access_key
        self.SecurityKey = security_key
        self.name = name

    def get_node(self):
        return Node(self.name, self.AccessKey, self.SecurityKey)

    def get_disk(self):
        return Disk(self.name, self.AccessKey, self.SecurityKey)

    def get_net(self):
        return Network(self.name, self.AccessKey, self.SecurityKey)

    def get_image(self):
        return Image(self.name, self.AccessKey, self.SecurityKey)
