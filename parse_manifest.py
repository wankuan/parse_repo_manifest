#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xml.dom.minidom
from xml.dom.minidom import parse



class parse_manifetst:
    # limit max include xml size
    include_max = 50
    include_current = 0
    git_name_list =[]
    git_localpath_list =[]
    branch_name = "\0"
    branch_name_flag = False
    remote_path = "\0"
    remote_path_flag = False
    remote_name = "\0"
    remote_name_flag = False
    def __init__(self):
        pass

    def get_git_name_list(self):
        return self.git_name_list
    def get_git_localpath_list(self):
        return self.git_localpath_list
    def get_branch_name(self):
        return self.branch_name
    def get_remote_path(self):
        return self.remote_path
    def get_remote_name(self):
        return self.remote_name
    # Use recursive methods to parse xml
    def parse(self, xml_name):
        domTree = parse(xml_name)
        rootNode = domTree.documentElement
        print("[info]start to parse xml,name:%s"%xml_name)
        # check node "manifest" exist
        if rootNode.nodeName == "manifest":
            # check include xml
            includes = rootNode.getElementsByTagName("include")
            if includes:
                for include in includes:
                    self.include_current += 1
                    if self.include_current > self.include_max:
                        print("[error]include xml over max size:%s"%self.include_max)
                        break
                    include_name = include.getAttribute("name")
                    print("[info]find the include xml, name:%s"%include_name)
                    self.parse(include_name)
            # parse xml
            remotes = rootNode.getElementsByTagName("remote")
            for remote in remotes:
                if self.remote_path_flag == False:
                    self.remote_path_flag = True
                    self.remote_path = remote.getAttribute("review")
                    print("[info]remote,review:%s"%self.remote_path)
                else:
                    print("[error]remote path has set, name:%s"%self.remote_path)
                if self.remote_name_flag == False:
                    self.remote_name_flag = True
                    self.remote_name = remote.getAttribute("name")
                    print("[info]remote,name:%s"%self.remote_name)
                else:
                    print("[error]remote name has set, name:%s"%self.remote_name)
                print("[info]remote,fetch:%s"%remote.getAttribute("fetch"))

            defaults = rootNode.getElementsByTagName("default")
            for default in defaults:
                if self.branch_name_flag == False:
                    self.branch_name_flag = True
                    self.branch_name = default.getAttribute("revision")
                    print("[info]default,revision:%s"%self.branch_name)
                    print("[info]default,remote:%s"%default.getAttribute("remote"))
                    print("[info]default,sync-j:%s"%default.getAttribute("sync-j"))
                else:
                    print("[error]defaults branch has set, name:%s"%self.branch_name)

            projects = rootNode.getElementsByTagName("project")
            for project in projects:
                path = project.getAttribute("path")
                name = project.getAttribute("name")
                self.git_localpath_list.append(path)
                self.git_name_list.append(name)
                print("[info]projects,path:%s"%path)
                print("[info]projects,name:%s"%name)
        else:
            print("repo xml format error, not find the TagName manifest")
        print("[info]end to parse xml,name:%s"%xml_name)

if __name__ == "__main__":
    init_xml = "test2.xml"
    handler = parse_manifetst()
    handler.parse(init_xml)
    print(handler.get_git_name_list())
    print(handler.get_git_localpath_list())
    print(handler.get_branch_name())
    print(handler.get_remote_path())
    print(handler.get_remote_name())