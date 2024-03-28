from django.db import models

# Create your models here.

class Employee(models.Model):
    TITLE_CHOICES = [
        ("PM", "Project Manager"),
        ("RD", "Research and Development"),
        ("BE", "Back-end Engineer"),
        ("FE", "Front-end Engineer"),
        ("SE", "Software Engineer"),
        ("EE", "Embedded Engineer"),
        ("UI", "User Interface"),
        ("UE", "User Experience"),
        ("QA", "Quality Assurance"),
        ("OP", "Operation"),
        ("DB", "Database Administrator")
    ]
    employee_id = models.IntegerField(blank=False, default=None, unique=True) # required
    first_name = models.CharField(max_length=30, blank=False, default=None) # required
    last_name = models.CharField(max_length=30, blank=False, default=None)   # required  
    # null-required or not in DB, blank-required or not in form
    hire_date = models.DateField(null=True) # optional
    email = models.EmailField(null=True, unique=True) # optional
    salary = models.FloatField(null=True) # optional
    title = models.CharField(null=True, max_length=2, choices=TITLE_CHOICES) # optional
    level = models.IntegerField(default=0) # optional
    # relationship
    department = models.ForeignKey("Department", null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['last_name', 'first_name']

    def hire_status(self):
        if not self.hire_date:
            return 'N/A'
        from datetime import datetime, timedelta
        if self.hire_date  > datetime.date(datetime.now() - timedelta(weeks=500)):
            return "Short-term(5-)"
        elif self.hire_date  < datetime.date(datetime.now() - timedelta(weeks=1000)):
            return "Long-term(10+)"
        else:
            return "Normal(5-10)"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
            
    def __str__(self):
        return self.full_name


# 1:1 relationship
class OneCard(models.Model):
    CARD_TYPES = [('VC', 'Virtual Card'), ('SC', 'Smart Card'), ('PC', 'Plastic Card')]
    number = models.IntegerField(blank=False, default=None, unique=True)
    card_type = models.CharField(max_length=2, choices=CARD_TYPES)
    issued_date = models.DateField(null=True)
    photo = models.BooleanField(default=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_card_type_display()}-{self.number}"


# M:1 relationship
class Department(models.Model):
    name = models.CharField(max_length=100, blank=False, default=None, unique=True)
    description = models.TextField()

    def __str__(self):
        return f'Department of {self.name}'


# M:1 relationship
class Report(models.Model):
    title = models.CharField(max_length=128, blank=False, default=None, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    report_date = models.DateField(null=True)
    content = models.TextField()

    def __str__(self):
        return f"Report \"{self.title}\" by {self.employee} on {self.report_date})"


# M:N between employees and projects
class Project(models.Model):
    name = models.CharField(max_length=128, blank=False, default=None, unique=True)
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return f'Project: {self.name}'


# ========================================================
# Exercises


class Location(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.address}, {self.city}"

class School(models.Model):
    SCHOOL_TYPES = [
        ('preliminary', 'Preliminary'),
        ('middle', 'Middle'),
        ('high', 'High'),
        ('others', 'Others')
    ]

    name = models.CharField(max_length=100)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=SCHOOL_TYPES)

    def __str__(self):
        return f"{self.name} ({self.type}) at {self.location}"

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    credit = models.IntegerField()
    teachers = models.ManyToManyField('Teacher')

    def __str__(self):
        return self.name


# ==== other examples ====
# ========================================================
    # class Meta:
    #     abstract = True # not to create DB table
    
# M:1
class Manufacturer(models.Model):
    pass
    class Meta:
        abstract = True

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    class Meta:
        abstract = True

# ========================================================
# M:N
class Topping(models.Model):
    pass
    class Meta:
        abstract = True

class Pizza(models.Model):
    toppings = models.ManyToManyField(Topping)
    class Meta:
        abstract = True

# ========================================================
# M:N and M:1
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

from datetime import date

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)
    class Meta:
        abstract = True

    def __str__(self):
        return self.headline

# ========================================================

# M:N with an intermediate model
class Person(models.Model):
    name = models.CharField(max_length=128)
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through="Membership")
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
    class Meta:
        abstract = True


# ========================================================
# M:1(publisher-books) and M:N(authors-books, books-stores)
class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    class Meta:
        abstract = True


class Publisher(models.Model):
    name = models.CharField(max_length=300)
    class Meta:
        abstract = True


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()
    class Meta:
        abstract = True


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)
    class Meta:
        abstract = True

# ========================================================
# 1:1 and M:1
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} the place"


class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
    class Meta:
        abstract = True

    def __str__(self):
        return "%s the restaurant" % self.place.name


class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    class Meta:
        abstract = True

    def __str__(self):
        return "%s the waiter at %s" % (self.name, self.restaurant)


# ========================================================

class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    class Meta:
        abstract = True
        ordering = ["headline"]

    def __str__(self):
        return self.headline


# ========================================================

class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        abstract = True
        ordering = ["title"]

    def __str__(self):
        return self.title


class Article1(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        abstract = True
        ordering = ["headline"]

    def __str__(self):
        return self.headline

# ========================================================            

from django.db import models

class Person(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    spouse = models.OneToOneField('self', on_delete=models.SET_NULL, blank=True, null=True)
    children = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
