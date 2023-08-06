#!/usr/bin/python3

import os
import sys
import argparse
import binascii

import pygit2   # pip3 install pygit2. Unfortunately, this does not include ssh support

import tdbase

tdbase_req_ver = "0.0.2"
if tdbase.__version__ < tdbase_req_ver:
    raise Exception("tdbase version %s too old, need at least %s" % (tdbase.__version__, tdbase_req_ver))

pygit2_req_ver = "0.28.2"
if pygit2.__version__ < pygit2_req_ver:
    raise Exception("old pygit2 %s, please update to at least %s" % (pygit2.__version__, pygit2_req_ver))

# if not pygit2.features & pygit2.GIT_FEATURE_SSH:
#    raise Exception("no ssh support in pygit2")




def myUidEncode(uid: bytes) -> str:
    if len(uid) != 8:
        raise Exception()
    return binascii.hexlify(uid).decode("ascii").upper()
def myUidDecode(txt: str) -> bytes:
    if len(txt) != 16:
        raise Exception()
    return binascii.unhexlify(txt)


def my_system(cmd):
    print ("*cmd", cmd)
    os.system(cmd)

def read_repos_file(fn:str):
    absfn = os.path.abspath(fn)
    _maindir, fn = os.path.split(absfn)

    p = tdbase.TDBParser()
    p.set_uid_funcs(myUidEncode, myUidDecode, 8)
    p.add_valid_record_types(["cfg", "repo"])

    p.add_record_schema("repo", {
            ("descr","R") : str,                # R means required. Must be in the data (will not be added)
            ("sync","") : [str],                # "" means optional. type is a list of str.
            ("branches","A") : {                   # A means will be added with default data if not there.
            ("", ""): {                           # all keys are allows for branches attr, but they value must confirm to below.
                ("path", "A"): str,                       # add branches.path, type str, if not exist.
                ("", ""): None,                          # and any other attribs are allowed, and can be any type (=None)
            }
        },
        ("", ""): str,                       # all other keys are allowed, but must be str
    })

    p.parse(absfn)
    p.map_records()
    p.section_records()
    p.check_schema()

    cfg = p.get_singleton_record("cfg")

    return cfg, p



def cmd_update_repos(repos_file_name: str, current_dir: str):
    cfg, p = read_repos_file(repos_file_name)
    url_base = cfg.attr["url"].value
    for r in p.iter_all_records("repo"):
        mapp = r.get_attrib_map_copy()

        # print (mapp)
        if not mapp["branches"]:
            continue # hack - should always get a dict here!

        for branch_name, v in mapp["branches"].items():
            if not v["path"]:
                continue
            repoPath = os.path.join(current_dir, v["path"])
            if not os.path.exists(repoPath):
                print ("Clone branch %s into %s:" % (branch_name, v["path"]))
                uid = r.get_uid_as_str()
                url = url_base+"/%s.git" % uid
                parentDir = os.path.split(repoPath)[0]
                if not os.path.exists(parentDir):
                    os.makedirs(parentDir)
                if branch_name=="master":
                    my_system("git clone %s %s" % (url, repoPath))
                else:
                    my_system("git clone -b %s %s %s" % (branch_name, url, repoPath))
            else:
                print ("Update branch %s in %s:" % (branch_name, v["path"]))

            # now pull/submodule update
            try:
                oldDir = os.getcwd()
                os.chdir(repoPath)
                my_system("git pull")
                my_system("git submodule update --init --recursive")
            finally:
                os.chdir(oldDir)

def cmd_writeback_repos(repos_file_name: str, current_dir: str):
    cfg, p = read_repos_file(repos_file_name)
    url_base = cfg.attr["url"].value
    p.set_sort(sort_records = "TN", sort_attribs = "K")
    for r in p.iter_all_records("repo"):
        mapp = r.get_attrib_map_copy()
        # assign name of record to path of master branch
        if not mapp["branches"]:
            continue # hack - should always get a dict here!
        if "master" in mapp["branches"]:
            if "path" in mapp["branches"]["master"]:
                r.set_record_name(mapp["branches"]["master"]["path"].replace("\\","/"))
    p.write_back()



def cmd_gen_rnd(repos_file_name: str, current_dir: str):
    r = os.urandom(8)
    print (binascii.hexlify(r).upper().decode("ascii"))

def old_handleRepos(reposFileName: str, current_dir: str):
    p = read_repos_file(repos_file_name)
    if 0:
        absfn = os.path.abspath(reposFileName)
        _maindir, fn = os.path.split(absfn)

        p = tdbase.TDBParser()
        p.set_uid_funcs(myUidEncode, myUidDecode, 8)
        p.add_valid_record_types(["repo"])

        p.add_record_schema("repo", {
                ("descr","R") : str,                # R means required. Must be in the data (will not be added)
                ("sync","") : [str],                # "" means optional. type is a list of str.
                ("branches","A") : {                   # A means will be added with default data if not there.
                ("", ""): {                           # all keys are allows for branches attr, but they value must confirm to below.
                    ("path", "A"): str,                       # add branches.path, type str, if not exist.
                    ("", ""): None,                          # and any other attribs are allowed, and can be any type (=None)
                }
            },
            ("", ""): str,                       # all other keys are allowed, but must be str
        })

        p.parse(absfn)
        p.map_records()
        p.section_records()
        p.check_schema()

    for r in p.iter_all_records():
        if r.recordType == "repo":
            uid = r.get_uid_as_str()
            #print (uid, r.recordName)
            mapp = r.get_attrib_map_copy()

            if not mapp["branches"]:
                continue  # hack, should not be needed. We should get an empty dict!
            for branch_name, v in mapp["branches"].items():
                # print (uid, k, v["path"])
                repoPath = os.path.join(current_dir, v["path"])
                if not os.path.exists(repoPath):
                    print ("")
                    url = "ssh://aprod/~/repos/%s.git" % uid
                    parentDir = os.path.split(repoPath)[0]
                    if not os.path.exists(parentDir):
                        os.makedirs(parentDir)
                    os.system("git clone %s %s" % (url, repoPath))
                    try:
                        oldDir = os.getcwd()
                        os.chdir(repoPath)
                        os.system("git submodule update --init --recursive")
                    finally:
                        os.chdir(oldDir)


                    if 0:

                        url = "ssh://git-aprod@10.66.6.1:2222/~/repos/%s.git" % uid
                        url = "ssh://git-aprod@a-prod.se:2222/~/repos/%s.git" % uid
                        url = "ssh://git-aprod@10.66.6.1/repos/%s.git" % uid
                        print ("%s does not exist, clone from server %s" % (repoPath, url))

                            #print("Cloning pygit2 over ssh with the username in the URL")
                            #keypair = pygit2.Keypair("git", "id_rsa.pub", "id_rsa", "")
                            #callbacks = pygit2.RemoteCallbacks(credentials=keypair)
                            # pygit2.clone_repository("ssh://git@github.com/libgit2/pygit2", "pygit2.git",
                            #                        callbacks=callbacks)

                            #keypair = pygit2.Keypair("git", "id_rsa.pub", "id_rsa", "")
                        keypair = pygit2.Keypair("git-aprod", "<id_rsa.pub>", "c:/Users/jeri/.ssh/id_rsa_git_private", "")
                        callbacks = pygit2.RemoteCallbacks(credentials=keypair)

                        pygit2.clone_repository(url, repoPath, checkout_branch=branch_name, callbacks=callbacks)



def main():
    parser = argparse.ArgumentParser(prog="mrm", description="Multi Repo Manager - handle several (git) repos")
    parser.add_argument("repo_list", type=str, help="list of repos")
    parser.add_argument("--cmd", type=str, help="command to run")
    args = parser.parse_args(sys.argv[1:])

    if args.cmd:
        cmd = args.cmd[0]
    else:
        print ("""Multi Repo Manager:
U.......update all repos
W.......write updates repo list to database
R.......generate random ID
>""", end="")
        cmd = input()
        if cmd:
            cmd = cmd[0]
        else:
            print ("No choice - exit")
            return

    cmd = cmd.upper()
    cwd = os.getcwd()
    if cmd=="U":
        cmd_update_repos(args.repo_list, cwd)
    elif cmd=="W":
        cmd_writeback_repos(args.repo_list, cwd)
    elif cmd=="R":
        cmd_gen_rnd(args.repo_list, cwd)
    else:
        print ("Unkown command '%s' - exit" % cmd)


main()
