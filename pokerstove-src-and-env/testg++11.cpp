
/************************************************************************* 
    > File Name: test.cpp 
    > Author: SongLee 
    > E-mail: lisong.shine@qq.com  
    > Created Time: 2014年03月23日 星期日 22时29分19秒 
    > Personal Blog: http://songlee24.github.io/ 
 ************************************************************************/  
#include<iostream>  
#include<cstring>  
#include<cctype>  
using namespace std;  
  
int main()  
{  
    string str("some string");  
    // range for 语句  
    for(auto &c : str)  
    {  
        c = toupper(c);  
    }  
    cout << str << endl;  
    return 0;  
}  
