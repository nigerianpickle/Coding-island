class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        result=[]

        for num in nums:

            tempList=nums.copy()
            tempList.remove(num)
            
            value=1
            for temp in tempList:
                value*=int(temp)
            result.append(value)


        return result
        