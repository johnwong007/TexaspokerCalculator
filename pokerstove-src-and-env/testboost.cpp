#include <boost/lexical_cast.hpp>
#include <iostream>
int main()
{
        using boost::lexical_cast;
        int a = lexical_cast<int>("123");
        double b = lexical_cast<double>("123.12");
        std::cout<<a<<std::endl;
        std::cout<<b<<std::endl;
        return 0;
}

//编译：g++ testboost.cpp -I$BOOST_INCLUDE -L$BOOST_LIB -o testboost
//执行：./testboost
