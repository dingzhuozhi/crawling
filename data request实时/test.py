import random
import time
from datetime import datetime


def merge(nums,left,mid,right):
    temp=[]
    l=left
    r=mid+1
    while l<mid and r<right:
        if nums[l]<=nums[r]:
            temp.append(nums[l])
            l+=1
        else:
            temp.append(nums[r])
            r+=1
    while l< mid:
        temp.append(nums[l])
    while r<right:
        temp.append(nums[r])
    nums[0:right+1]=temp



def merge_sort(nums,left,right):
    if left<right:
        mid=left+(right-left)//2
        merge(nums,)