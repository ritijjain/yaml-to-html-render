from django.db import models
from render_doc.utils import id_8
import yaml
from github import Github
from simple_history.models import HistoricalRecords
import os

class Tag(models.Model):
    # id = models.CharField(max_length=16, primary_key=True, editable=False, default=id_8)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

class Block(models.Model):
    # id = models.CharField(max_length=16, primary_key=True, editable=False, default=id_8)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=256, null=True)
    data = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=64, null=True, blank=True)
    template = models.CharField(max_length=255, null=True, blank=True)
    public = models.BooleanField(default=False)
    history = HistoricalRecords()

    
    def __str__(self):
        return f'{self.title} id={self.id}'

    @property
    def parse_yaml(self):
        return yaml.load(self.data)

    # Function from: https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries/15836901#15836901
    @classmethod
    def data_merge(cls, a, b):
        '''merges b into a and return merged result

        NOTE: tuples and arbitrary objects are not handled as it is totally ambiguous what should happen'''
        key = None
        # ## debug output
        # sys.stderr.write("DEBUG: %s to %s\n" %(b,a))
        try:
            if a is None or isinstance(a, (str, int, float)):
                # border case for first run or if a is a primitive
                a = b
            elif isinstance(a, list):
                # if b is a list, merge operation recursively
                if isinstance(b, list):
                    # merge up to the last item of the shorter list
                    for i in range(min(len(a), len(b))):
                        a[i] = cls.data_merge(a[i], b[i])
                    # append rest
                    for i in range(min(len(a), len(b)), max(len(a), len(b))):
                        a.append(b[i])
                else:
                    a.append(b)
            elif isinstance(a, dict):
                # dicts must be merged
                if isinstance(b, dict):
                    for key in b:
                        if key in a:
                            a[key] = cls.data_merge(a[key], b[key])
                        else:
                            a[key] = b[key]
                else:
                    raise Exception('Cannot merge non-dict "%s" into dict "%s"' % (b, a))
            else:
                raise Exception('NOT IMPLEMENTED "%s" into "%s"' % (b, a))
        except TypeError as e:
            raise Exception('TypeError "%s" in key "%s" when merging "%s" into "%s"' % (e, key, b, a))
        return a
    
    @property
    def data_inheritance(self):
        if self.parent:
            # return {**self.parent.data_inheritance, **self.parse_yaml}
            return self.data_merge(self.parent.data_inheritance, self.parse_yaml)
        else:
            return self.parse_yaml 


    def gh_api_auth(self):
        self.gh = Github(os.environ['GH_TOKEN'])
    
    def gh_update_resume(self, file):
        self.gh_api_auth()
        repo = self.gh.get_repo('ritijjain/ritijjain.com')
        contents = repo.get_contents('resume.html')
        response = repo.update_file(contents.path, 'Via rj-portal: Updated resume', file, contents.sha, branch='master')
        return response

