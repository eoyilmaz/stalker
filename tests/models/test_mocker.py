#-*- coding: utf-8 -*-



import mocker

mocker_obj = mocker.Mocker()
obj = mocker_obj.mock()

obj.hello()
mocker_obj.result("Hi!")
mocker_obj.count(0,1000)

mocker_obj.replay()

obj.hello()
#'Hi!'

#obj.bye()
#Traceback (most recent call last):
#...
#mocker_obj.MatchError: [Mocker] Unexpected expression: obj.bye

#mocker_obj.restore()
#mocker_obj.verify()
