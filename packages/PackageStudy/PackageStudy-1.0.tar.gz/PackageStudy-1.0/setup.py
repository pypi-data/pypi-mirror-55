#coding = utf-8
from setuptools import setup, find_packages  
  
setup(  
     name = "PackageStudy",  
     version = "1.0",  
     #keywords = ("test", "xxx"),  
     #description = "eds sdk",  
     #long_description = "eds sdk for python",  
     #license = "MIT Licence",  
   
     url = "http://test.com",  
     author = "fcsfhxfjz",  
     author_email = "562367673@qq.com",  
   
     packages = find_packages('src'), 
	 package_dir = {"":"src"},
     #include_package_data = True,  
     #platforms = "any",  
     #install_requires = [],  
   
     #scripts = [],   
 )  