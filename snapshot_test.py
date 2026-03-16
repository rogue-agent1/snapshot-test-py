#!/usr/bin/env python3
"""Snapshot testing — save and compare output."""
import json, os, sys, hashlib

class SnapshotTester:
    def __init__(self,snap_dir=".snapshots"):
        self.dir=snap_dir; os.makedirs(snap_dir,exist_ok=True)
        self.results={"passed":0,"updated":0,"failed":0}
    def _path(self,name): return os.path.join(self.dir,f"{name}.snap")
    def assert_match(self,name,value,update=False):
        path=self._path(name)
        current=json.dumps(value,indent=2,sort_keys=True,default=str)
        if not os.path.exists(path) or update:
            with open(path,"w") as f: f.write(current)
            self.results["updated"]+=1; return True
        with open(path) as f: saved=f.read()
        if current==saved: self.results["passed"]+=1; return True
        self.results["failed"]+=1
        print(f"  ❌ Snapshot '{name}' mismatch"); return False
    def summary(self):
        return f"  Snapshots: {self.results['passed']} passed, {self.results['updated']} updated, {self.results['failed']} failed"

if __name__ == "__main__":
    import tempfile
    st=SnapshotTester(os.path.join(tempfile.mkdtemp(),".snap"))
    st.assert_match("user",{"name":"Alice","age":30,"roles":["admin"]})
    st.assert_match("config",{"debug":True,"port":8080})
    # Second run matches
    st.assert_match("user",{"name":"Alice","age":30,"roles":["admin"]})
    # This would fail if data changed
    print(st.summary())
