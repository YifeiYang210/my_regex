import sys
sys.setrecursionlimit(10000)

# write your code here
def compare_char(rchar, ichar):
    """ 
    接受两个字符，一个regex：rchar和一个input：ichar
    将 regex 与 input 进行比较，并返回一个布尔值，表示是否存在匹配
    Accepts two characters: rchar (regex) and ichar (input)
    Compares the regex character with input character, returns a boolean indicating match status

    测试样例：
    Test cases:
    a|a -> True
    .|a -> True
    |a  -> True
    |   -> True
    a|  -> False
    """
    # 空的正则表达式始终返回 True 。
    # Empty regex always returns True
    if rchar == '':
        return True
    # 空的输入字符串始终返回 False ，除非正则表达式也是空的。
    # Empty input returns False unless regex is also empty
    elif ichar == '':
        return False

    # 点作为通配符，这里可以匹配任何输入
    # Dot wildcard matches any input character
    if rchar == '.':
        return True
    else:
        return rchar == ichar


def match(rstr, istr):
    """
    匹配等长字符串，通过递归来实现
    为实现完全匹配，要么每个字符对相同，要么正则表达式中包含通配符
    Recursive string matching with escape character handling
    
    测试样例：
    Test cases:
    Input: 'colou?r|color'       Output: True
    Input: 'colou?r|colouur'     Output: False
    """
    # 如果正则表达式已被完全消耗返回 True。
    # Base case: empty regex matches anything
    if rstr == '':
        return True
    # 如果正则表达式未被完全消耗，但输入字符串已被消耗返回 False。
    # Handle end-of-string anchor
    elif istr == '':
        # 如果正则表达式只剩$说明匹配成功（暂时不考虑转义字符）
        return rstr == '$'

    # 如果存在转义字符 \ （在编程语言里需写作\\），则下一个字符需要匹配
    # Handle escape sequences
    if rstr[0] == '\\':
        # 如果转义字符后跟着点字符，则元字符不发挥原本的作用，变成文本字符
        # Match escaped metacharacters literally
        if rstr[1:2] in ['.', '?', '+', '*', '\\', '^', '$']:
            return istr[0] == rstr[1:2] and match(rstr[2:], istr[1:])
            
    # 如果正则表达式与输入字符串的第一个字符不匹配返回 False
    # Handle non-matching characters
    if not compare_char(rstr[0], istr[0]):
        # 如果存在量词?和*，是可以1个也不匹配的
        # Handle zero-match cases for ? and *
        if rstr[1:2] in ['?', '*']:
            #  假设?或*前的字符是未匹配的情况，那么检索式跳过?或*，还是匹配输入串的当前字符
            return match(rstr[2:], istr[0:])

        else:
            return False
        
    # 如果上述情况都不适用（首字符匹配），则递归应继续，直到通过切片完全消耗正则字符串对。
    # Handle matching characters with quantifiers
    else:
        # 如果存在量词?，可以匹配0-1个 (前面已经给出匹配0个，匹配1个就是rstr[0]和istr[0]匹配，下一步跳到istr[1:])
        # Handle ? quantifier cases
        if rstr[1:2] == '?':
            return match(rstr[2:], istr[1:])
        # 如果存在量词+和*，可以匹配1到多个 (前面已经给出匹配0个，匹配1个同上，匹配多个就是rstr[0]不跳到下一步，始终匹配)
        # Handle + and * quantifiers
        if rstr[1:2] in ['+', '*']:
            return match(rstr[2:], istr[1:]) or match(rstr, istr[1:])
        # 如果不存在量词，则匹配1个
        # Default case: match single character
        return match(rstr[1:], istr[1:])


def compare_unequal_length_str_part_with_escape(rstring, istring):
    """
    匹配指定特定开头和结尾位置的不等长字符串，迭代实现
    如果输入串指定位置存在正则串的模式返回True
    Partial matching for unequal-length strings with anchors
    
    测试样例：
    Test cases:
    Input: '^app|apple' -> True
    Input: 'le$|apple' -> True
    """
    #  空搜索串或仅带有开头结尾匹配符号返回True
    # Handle empty regex special cases
    if rstring == '' or rstring == '^' or rstring == '$':
        return True

    # 如果有^，则需要匹配开头
    # Handle start anchor
    if rstring[0] == '^':
        return match(rstring[1:], istring)
    
    # 如果没有^：需要推进输入字符串，查找是否有匹配串
    # Iterate through input string for partial matches
    for i in range(len(istring)):
        if match(rstring, istring[i:]):
            return True
    
    # 如果达到字符串的末尾，还没有匹配，则返回False
    # No matches found
    return False 

#  6. 测试不等长带有起始结束匹配和量词+?*以及反义字符符号的字符串是否匹配
# Main entry point: process input and run matching
regex, input_s = input().split('|', 1)
print(compare_unequal_length_str_part_with_escape(regex, input_s))
