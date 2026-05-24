


class BlogTypes:
    article: int = 0
    wiki: int = 3
    thread: int = 4


class WikiPermission:
	Anyone: int = 1
	AdminOnly: int = 3
      
class ArticlePermission:
	Anyone: int = 1
	AdminOnly: int = 3
	
class ThreadsPermission:
	Anyone: int = 1
	AdminOnly: int = 3