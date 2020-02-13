### All responses will have the following form
'''json
{
 "attribute":"data"
}
'''
###Usage 

GET METHODS : 
  * Url '/api/trending_repos' --> selects the languages used by the most trending repositories
  in the last 30 days in order. 
  
 ###### ***response ***
  '''json 
  {
  
    "ranking" : "language_used"
  
  }
  '''
 
  * URL '/api/repositories/< lang >' --> Selects the name of the repositories
  that use the language entered by the user among the most trending repositories of the last 30 days. 
  
  ######***response ***
  
  '''json 
  {
  
    "ranking" : "repository_name"
  
  }
  '''
  
  * Url '/api/repositories/number/< lang >' --> Returns the number of repositories that use a language  
   
   ######***response ***
  
  '''json 
  {
  
    "number_repos" : "number"
  
  }
  '''