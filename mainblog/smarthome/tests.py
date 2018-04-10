from django.test import TestCase

# Create your tests here.

pwd="1235789"
new_pwd=""
for i in range(len(pwd)):
    new_pwd+=str(int(pwd[i])-1)
print(new_pwd)