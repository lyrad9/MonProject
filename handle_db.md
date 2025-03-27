# Import the models we created from our "news" app

> > > from news.models import Article, Reporter

# No reporters are in the system yet.

> > > Reporter.objects.all()
> > > <QuerySet []>

# Create a new Reporter.

> > > r = Reporter(full_name="John Smith")

# Save the object into the database. You have to call save() explicitly.

> > > r.save()

# Now it has an ID.

> > > r.id
> > > 1

# Now the new reporter is in the database.

> > > Reporter.objects.all()
> > > <QuerySet [<Reporter: John Smith>]>

# Fields are represented as attributes on the Python object.

> > > r.full_name
> > > 'John Smith'

# Django provides a rich database lookup API.

> > > Reporter.objects.get(id=1)
> > > <Reporter: John Smith>
> > > Reporter.objects.get(full_name**startswith="John")
> > > <Reporter: John Smith>
> > > Reporter.objects.get(full_name**contains="mith")
> > > <Reporter: John Smith>
> > > Reporter.objects.get(id=2)
> > > Traceback (most recent call last):

    ...

DoesNotExist: Reporter matching query does not exist.

# Create an article.

> > > from datetime import date
> > > a = Article(
> > > ... pub_date=date.today(), headline="Django is cool", content="Yeah.", reporter=r
> > > ... )
> > > a.save()

# Now the article is in the database.

> > > Article.objects.all()
> > > <QuerySet [<Article: Django is cool>]>

# Article objects get API access to related Reporter objects.

> > > r = a.reporter
> > > r.full_name
> > > 'John Smith'

# And vice versa: Reporter objects get API access to Article objects.

> > > r.article_set.all()
> > > <QuerySet [<Article: Django is cool>]>

# The API follows relationships as far as you need, performing efficient

# JOINs for you behind the scenes.

# This finds all articles by a reporter whose name starts with "John".

> > > Article.objects.filter(reporter**full_name**startswith="John")
> > > <QuerySet [<Article: Django is cool>]>

# Change an object by altering its attributes and calling save().

> > > r.full_name = "Billy Goat"
> > > r.save()

# Delete an object with delete().

> > > r.delete()
