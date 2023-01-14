from xml.dom import minidom
from os.path import exists
from pulp import *

import numpy as np
import argparse

skribblIOCharLimit = 20000

parser = argparse.ArgumentParser(
    description='Generate a randomized list of items for skribbl.io from a fandom.'
)
parser.add_argument('fandom', type=str, help='The fandom to generate items from.')
parser.add_argument('category', type=str, help='The category to generate items from.', nargs='+')

args = parser.parse_args()

def getNodeText(node):
    nodelist = node.childNodes
    result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    return ''.join(result)

def main():
    if not exists(args.fandom + '.xml'):
        os.system('python3 ScrapeFandom\\ScrapeFandom.py ' + args.fandom)
        
    parser = minidom.parse(args.fandom + '.xml')
    itemList = []
    
    for element in parser.getElementsByTagName('text'):
        elementText = getNodeText(element)
        itemName = getNodeText(element.parentNode.parentNode.getElementsByTagName('title')[0])
        
        if ('[[Category:' + ' '.join(args.category) + ']]')  in elementText:
            itemList.append(itemName)
            
    np.random.shuffle(itemList)
    
    validIndexEnd = 0
    totalCharacterCount = 0
    
    for i in range(len(itemList)):
        if totalCharacterCount + len(itemList[i]) > skribblIOCharLimit:
            validIndexEnd = i
            break
        totalCharacterCount += len(itemList[i])
   
    if validIndexEnd != 0:
        del itemList[validIndexEnd:]
        
    itemListFile = open(args.fandom + '_list.txt', 'w')
    itemListFile.write(', '.join(itemList))
                    
if __name__ == '__main__':
    main()