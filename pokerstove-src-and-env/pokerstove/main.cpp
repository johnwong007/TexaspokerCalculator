#include <iostream>
#include <vector>
#include <boost/program_options.hpp>
#include <pokerstove/penum/ShowdownEnumerator.h>
#include <math.h>

using namespace pokerstove;
namespace po = boost::program_options;
using namespace std;

double round(double r)
{
    return (r > 0.0) ? floor(r + 0.5) : ceil(r - 0.5);
}

int main(int argc, char** argv) {
  po::options_description desc("ps-eval, a poker hand evaluator\n");

  desc.add_options()("help,?", "produce help message")
      ("game,g", po::value<string>()->default_value("h"), "game to use for evaluation")
      ("board,b", po::value<string>(), "community cards for he/o/o8")
      ("dead,d", po::value<string>(), "dead cards for he/o/o8")
      ("hand,h", po::value<vector<string>>(), "a hand for evaluation")
      ("quiet,q", "produces no output");

  // make hand a positional argument
  po::positional_options_description p;
  p.add("hand", -1);

  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv)
                .style(po::command_line_style::unix_style)
                .options(desc)
                .positional(p)
                .run(),
            vm);
  po::notify(vm);

  // check for help
  if (vm.count("help") || argc == 1) {
    cout << desc << endl;
    return 1;
  }

  // extract the options
  string game = vm["game"].as<string>();
  string board = vm.count("board") ? vm["board"].as<string>() : "";
  string dead = vm.count("dead") ? vm["dead"].as<string>() : "";
  vector<string> hands = vm["hand"].as<vector<string>>();

  bool quiet = vm.count("quiet") > 0;
  
  // allocate evaluator and create card distributions
  boost::shared_ptr<PokerHandEvaluator> evaluator =
      PokerHandEvaluator::alloc(game);
  vector<CardDistribution> handDists;
  for (const string& hand : hands) {
    handDists.emplace_back();
    handDists.back().parse(hand);
  }

  // fill with random if necessary
  if (handDists.size() == 1) {
    handDists.emplace_back();
    handDists.back().fill(evaluator->handSize());
  }
  
  //int distsLen = handDists.size();
  //string deadstr = "jc";
  //for (int i = 0 ; i < distsLen ; i++) {
  //    handDists[i].removeCards(CardSet(deadstr));
  //    cout << handDists[i].str() << endl;
  //}
  //cout << "game is " << game << endl;
  //cout << "board is " << board << endl;
  //cout << "dead is " << dead << endl;
 
  // calcuate the results and print them
  ShowdownEnumerator showdown;
  vector<EquityResult> results =
      showdown.calculateEquity(handDists, CardSet(board), evaluator, CardSet(dead));

  double total = 0.0;
  for (const EquityResult& result : results) {
    total += result.winShares + result.tieShares;
  }
  cout<<"[";
  if (!quiet) {
      for (size_t i = 0; i < results.size(); ++i) {
        cout<<"[";
        double equity = (results[i].winShares + results[i].tieShares) / total;
        double win = results[i].winShares / total;
        double tie = results[i].tieShares / total;
        
        equity = round(equity*1e4)/1e4;
        char buf[10];
        sprintf(buf, "%.2f", equity);
        sscanf(buf, "%f", &equity);
        win = round(win*1e4)/1e4;
        char buf1[10];
        sprintf(buf1, "%.2f", win);
        sscanf(buf1, "%f", &win);
        tie = round(tie*1e4)/1e4;
        char buf2[10];
        sprintf(buf2, "%.2f", tie);
        sscanf(buf2, "%f", &tie);

        if(equity<0.00005){
            equity = 0;
        }
        if(win<0.00005){
            win = 0;
        }
        if(tie<0.00005){
            tie = 0;
        }
        string handDesc =
            (i < hands.size()) ? "The hand " + hands[i] : "A random hand";
        cout << equity * 100. << "," << win*100. << "," << tie*100.; 
        cout<<"]";
        if(i!=results.size()-1){
            cout << ",";
        }
        //cout << handDesc << " has " << equity * 100. << " % equity ("
        //<< results[i].str() << ")" << endl;
      }
  }
  cout<<"]";
}
