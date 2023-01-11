import sys
import os
from columnar import columnar
class Dataset:
    """Main class"""

    def grouping_dictionary(self,l):
        result = {}
        for k, v in l:
            result.setdefault(k, []).append(v)
        return result
    def __init__(self,path):
        """Main constructor"""
        self.path = path
        self.file_stats = {}
        self.totalsize = 0
        self.totdirs = 0
        self.totalfiles = 0
        self.filetype_nil_count=0
        self._process_entry(self);

    def _process_entry(self, entry):
        Size = [];
        List = [];
        dict = [];
        # Creating the iteratable object
        path_iter = os.scandir(self.path)
        for entry in path_iter:
            self.totalsize += os.path.getsize(entry)
            if entry.is_dir():
                self.totdirs  += 1
            if entry.is_file():
                self.totalfiles+=1
                File_Name = str(entry.name).split('.')
                File_Name = File_Name[-1]
                dict.append((File_Name, entry.stat().st_size))
            dict2 = {}
            dict2 = self.grouping_dictionary(dict)
            headers = ['File Type', 'File_Count', 'Max_FileSize_MB', 'Min_FileSize_MB', 'Average_FileSize_MB']
            data = []
            # print("File Type\tFile_Count\tMaxFileSize\tMinFileSize\tAverage File Size")
        for key in dict2:
            temp = []
            temp.append(key)
            temp.append(len(dict2[key]))
            temp.append(max(dict2[key])/1024/1000)
            temp.append(min(dict2[key])/1024/1000)
            temp.append((sum(dict2[key]) / len(dict2[key]))/1024/1000)
            data.append(temp)
        self.table = columnar(data, headers, no_borders=False)



    def __str__(self):
       return """Dataset Path: {path}]\n tot size(MB): {totsize}
                    tot dirs: {totdirs} tot files: {totfiles}
                    nil_file_type count: {nilcount}
                    file stats:\n{stats}""".format(path=self.path,

                                                  totsize=(self.totalsize // (1024 * 1024)),
                                                  totdirs=self.totdirs,
                                                  totfiles=self.totalfiles,
                                                  nilcount=self.filetype_nil_count,
                                                  stats=self.table
                                                  )



if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: python self.py path')

    path = sys.argv[1:]
    path=' '.join(path)
    print(path)
    obj = Dataset(path)
    print(obj)




