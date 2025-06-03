# Best Time to Buy and Sell Stock
# Solved 
# You are given an integer array prices where prices[i] is the price of NeetCoin on the ith day.

# You may choose a single day to buy one NeetCoin and choose a different day in the future to sell it.

# Return the maximum profit you can achieve. You may choose to not make any transactions, in which case the profit would be 0.

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        minPrice=10000000000000000
        maxPrice=-1000000000000000

        maxProfit=0
        for price in prices:
            if price<minPrice:
                minPrice=price

            profit=price-minPrice

            if profit>0:
                print(maxProfit)
                if profit>maxProfit:
                    maxProfit=profit

                
            

        return maxProfit






        