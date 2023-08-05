# Template-Nest Templating System

## TL;DR
You should definitely use Template-Nest because it's the most logical templating system in existence. 

* Create templates that have no code in them whatsoever. No "template ifs", "template loops". No "template includes". Nothing but holes to fill in.
* No code in your templates means they are language independent. Use the same templates with Java, Ruby, Perl, Javascript...
* If templating html, produce only ordinary html files that can be displayed independently in a browser. (ie. no files with weird extensions)
* Build views as a tree structure of templates (exactly as the DOM does!) limiting the number of templates needed and avoiding repetition.
* There is no "template language" to use or learn
* Eliminate the confusion of where to put processing. Get rid of the mess this confusion produces.

For intrigue, also see: "Building a template-less platform with Template-Nest" at the bottom of this page.

## SYNOPSIS

~~~html
	<!-- page.html -->
	<html>
		<head>
			<style>
				div { 
					padding: 20px;
					margin: 20px;
					background-color: yellow;
				}
			</style>
		</head>

		<body>
			<% contents %>
		</body>
	</html>
~~~ 

```html
	<!-- box.html -->
	<div>
		<% title %>
	</div>
```

```python

    from template_nest import Nest

	nest = Nest({
		template_dir => '/html/templates/dir',
        fixed_indent => 1
	})

	page = {
		'NAME': 'page',
		'contents': [{
			NAME => 'box',
			title => 'First nested box'
		}]
	}

	page[ 'contents' ].append({
		NAME => 'box',
		title => 'Second nested box'
	})

	print( nest.render( page ) )
```
	
### Output:

```html
    <html>
	    <head>
		    <style>
			    div { 
				    padding: 20px;
				    margin: 20px;
				    background-color: yellow;
			    }
		    </style>
	    </head>

	    <body>	    
            <div>
	            First nested box
            </div>
            <div>
	            Second nested box
            </div>
	    </body>
    </html>
```




## In depth

So admittedly my first statement on this page is a bold claim. Of course this is just my (narcissistic?) opinion - but read on to see if you agree.

I originally developed Template-Nest in Perl (see [here](https://metacpan.org/pod/Template::Nest). However, Template-Nest is a philosophy more than anything, and as such is language independent. (In fact, language independence is a key feature of Template-Nest as I am about to explain!)

I decided to port it over to Python for several reasons:

* I want to use the same templates with a Django project that are already being used in a Perl project. (The most practical reason).
* I think this is a great first module to get my feet wet publishing on PyPI. (The most humble reason).
* I want this templating philosophy to take over the world. (The most ambitious reason!)

Seriously though, regarding the last point: Even if this particular module does not get adopted (which it probably won't), it would be great if at least some people somewhere gained even a tiny modicum of exposure to the underlying philosophy. Even if all you do is read this documentation, and go away and think about what you read, then I would regard this exercise as having been worthwhile.

This isn't because I have some lofty goal of wanting to improve humanity. The reason is much more personal and straightforward: I am tired of tearing my hair out wading through messy, ugly templates! As a professional coder, I have to deal with these damn things on a daily basis, and sigh and groan to myself as I believe there is a better way. Please for the sake of sanity, stop torturing me with these gargantuan spaghetti heaps. Consider using Template-Nest instead.

# So what's the problem?

I think there are actually 2 problems:

1. Everyone is busily stuffing their "templates" full of code. I believe this

    * is not a good idea
    * violates MVC (sorry, but you haven't actually separated control from view)
    * means you probably need to learn a new mini language (the "templating language") on top of Python and/or whatever else.
    * makes displaying your raw template (e.g. in a browser) difficult (the browser can't handle `if`,`then` etc. statements written in your "templating language"
    * gives you an awkward file type with an uncomfortable extension (e.g. see [this debate](https://stackoverflow.com/questions/2035362/django-template-file-extension-preference) on the confusion of what extension is best to use for django templates.)
    * makes editing your raw template difficult (you have a mixture of markup and code, so which syntax highlighter do you pick?)
    * most importantly - because this is what causes the mess - raises the question of what is "program processing" vs. what is "template processing". Really, if you are going to have "template processing", then at a minimum you need a guideline as to how to identify it. If you don't have one (and most systems don't because if you are already putting code in templates, you probably haven't thought much about consequences), then the result is a mess: in one template you've got an `if`,`then` structure, while in another that same logic is missing because the coder decided to put it in the "program processing" and hand the template the result. Now add in "template loops" and whatever other nonsense your "templating language" provides, and then multiply it by hundreds of templates. The outcome is total incomprehensibility.

2. Most templating systems produce *tightly coupled* templates

    This is an issue I wasn't even really aware of until I discovered Template-Nest **doesn't** do this, and then noticed how much better it was without the coupling. So what do I mean by *tightly coupled*? Let's take Django. The [Tutorials Point documentation on Django templates](https://www.tutorialspoint.com/django/django_template_system.htm) helpfully tells us "A templating system cannot be complete without template inheritance". No disrespect to Tutorials Point here; they have great tutorials, and they are just echoing the commonly held view. But it is wrong! You *can* design a templating language without template inheritance. Template-Nest is one such templating system!

    Basically most templating systems encourage you to refer to templates from other templates. This might be done with an "include" - something like this:

    ~~~html
     <!-- page.djt -->

        <div>Main Page Title</div>

        <div>{% include content.djt %}</div>

        <div>Some Footer</div>
    ~~~

    or with an "extend", like this:

    ~~~html
     <!-- child.djt --->
        {% extends parent.djt %}

        <div>Some Childish Stuff</div>

    ~~~

    In either case, you are essentially hard coding the relationship between your templates *inside* the templates. E.g. what happens if one time you want to include `other_content.djt` instead of `content.djt` in `page.djt` above? Yes you can do it with inheritance, but it's ugly and you are going to end up with one more template. 

The point being, in my opinion the relationship between templates is *also control processing*. The templates should not know about each other. It is the job of the controller to decide how to slot the templates together. So template `include` and `extends` should also not be necessary.

# How is Template-Nest different?

I think the concept of templating originally started with the "one template per view" (or perhap "page") paradigm. It's compelling to save files with names like "home_page_template" etc. So if you do that, you need to have processing in your template, because it's going to have stuff in it thats the same as "blog_page_template". It seems as if most templating systems start with this premise, and the question of how to combine templates is almost tacked on as an afterthought.

With Template-Nest we deal with the issue of combining templates first and foremost; and we assume you are going to create tree-like structures of templates. Remember, HTML is tree structured, the browser treats pages as trees of elements (ie the DOM), so why are we attempting to create what's sent to the client from a monolithic slab? No wonder our templates end up stuffed full of code.



## AN EXAMPLE

Lets say you have a template for a letter (if you can remember what that is!), and a template for an address. Using the standard Django templating system you might do something like this:

### in letter.html

```

    {% include address.djt %}

    Dear {{username}}

    ....
```


However, in Template-Nest there's no `include` - there are only tokens to fill in, so you would have

### in letter.html:

```html
    <!--% address %-->

    Dear <!--% username %-->

    ...
```

I specify that I want to use `address.html` when I fill out the template, thus:

```python
    letter = {
        'NAME': 'letter',      # this specifies "letter.html" (provided template_ext=".html")
        'username': 'billy',  
        'address': {
            'NAME': 'address', #  "address.html" 
                               
            # any other variables in 'address.html'
        }
    }

    print( nest.render( letter ) )
```


This is much better, because now `letter.html` is not hard-coded to use `address.html`. You can decide to use a different address template without needing to change the letter template.

Commonly used template structures can be labelled (`main_page` etc.) stored in your code in functions, dicts, object attributes or whatever method seems the most convenient.

## Another example

The idea of a "template loop" comes from the need to e.g. fill in a table with an arbitrary number of rows. So using Django's standard templating system you might do something like: 

### in employee_list.djt:

```html
    <table>
        <tr>
            <th>Name</th><th>Job</th>
        <tr>

        {% for employee in employees %}
            <tr>
                <td>{{ employee.name }}</td>
                <td>{{ employee.job_title }}</td>
            </tr>
        {% endfor %}
    </table>
```

### in the python:

```python

    employee_info = [
        {'name': 'Sam', 'job': 'programmer'}, 
        {'name': 'Steve', 'job': 'soda jerk'}
    ]
    html = render( request, "employee_list.djt", { 'employee_info' : employee_info })

    print( html )
```

### output:
```html
    <table>
        <tr>
            <th>Name</th><th>Job</th>
        </tr>
        <tr>
            <td>Sam</td><td>programmer</td>
        </tr>
        <tr>
            <td>Steve</td><td>soda jerk</td>
        </tr>
    </table>
```


That's great - but why have the loop inside the template? If the table row is going to be repeated an arbitrary number of times, doesn't it make sense that this row should have its own template? In the Template-Nest scheme, this would look like:

### table.html:

```html
    <table>
        <tr>
            <th>Name</th><th>Job</th>
        </tr>

        <!--% rows %-->

    </table>
```

### table_row.html:

```html
    <tr>
        <td><!--% name %--></td>
        <td><!--% job %--></td>
    </tr>
```

### and in the Python:

```python

    table = {
        'NAME': 'table',
        'rows': [{
            'NAME': 'table_row',
            'name': 'Sam',
            'job': 'programmer'
        }, {
            'NAME': 'table_row',
            'name': 'Steve',
            'job': 'soda jerk'
        }]
    }

    nest = Nest({
        'token_delims': ['<!--%','%-->']
    })

    print( nest.render( table ) )
```

Now the processing is entirely in the Python. Of course, if you need to fill in your table rows using a loop, this is easy:

```python
    rows = []

    for item in data:

        rows.append({
            'NAME': 'table_row',
            'name': item.name,
            'job': item.job
        })


    table = {

        'NAME': 'table',
        'rows': 'rows'

    }

    nest = Nest({
        'token_delims': ['<!--%','%-->']
    })

    print nest.render( table )
```

Template-Nest is far simpler, and makes far more sense!




## METHODS


### constructor

```python
    nest = Nest( args )
```

args is a dict that can contain keys corresponding to any of the methods Template-Nest accepts. For example you can do:

```python
    nest = Nest({ template_dir => '/my/template/dir' })
```

or equally:

```python
    nest = Nest()
    nest.template_dir( '/my/template/dir' )
```


### comment_delims

Use this in conjunction with show_labels. Get/set the delimiters used to define comment labels. Expects a 2 element list. E.g. if you were templating javascript you could do:

```python

    nest.comment_delims( ['/*', '*/'] )

```
    
Now your output will have labels like

```javascript

    /* BEGIN my_js_file */

    // your code

    /* END my_js_file */

```

You can set the second comment token as an empty string if the language you are templating does not use one. E.g. for Python:

```python

    nest.comment_delims([ '#','' ])

```

### defaults

Provide a dict of default values to have Template-Nest auto-fill matching parameters (no matter where they are found in the template tree). For example:


### box.html:

```html

<div class='box'>
    <!--% contents %-->
</div>

```

### link.html:

```html

    <a href="<!--% soup_website_url %-->">Soup of the day is <!--% todays_soup %--> !</a>

```

### in the Python:

```python

    nest = Nest({
        'token_delims': ['<!--%','%-->']
    })

    my $page = {
        NAME => 'box',
        contents => {
            NAME => 'link',
            todays_soup => 'French Onion Soup'
        }
    }

    html = nest.render( page )

    print( html )

```

### this prints:
    
```html

<div class='box'>
    <a href="">Soup of the day is French Onion Soup !</a>
</div>

```

Note the blank "href" value - because we didn't pass it as a default, or specify it explicitly.
Now lets set some defaults:

```python

    nest.defaults({
        'soup_website_url': 'http://www.example.com/soup-addicts',
        'some_other_url': 'http://www.example.com/some-other-url' #any default that doesn't appear
    })                                                           #in any template is simply ignored

    html = nest.render( page )
```

This time "href" is populated:

```html

<div class='box'>
    <a href="http://www.example.com/soup-addicts">Soup of the day is French Onion Soup</a>
</div>

```

Alternatively provide the value explicitly and override the default:

```python

    page = {
        'NAME': 'box',
        'contents': {
            'NAME': 'link',
            'todays_soup': 'French Onion Soup',
            'soup_website_url': 'http://www.example.com/soup-url-override'
        }
    }

    html = nest.render( page )

```

The result:

```html

    <div class='box'>
        <a href='http://www.example.com/soup-url-override'
    </div>

```

ie. `defaults` allows you to preload your `nest` with any values which you expect to remain constant throughout your project.


You can also *namespace* your default values. Say you think it's a better idea to differentiate parameters coming from config from those you are expecting to explicitly pass in. You can do something like this:

### link.html:

```html
    <a href="<--% config.soup_website_url %-->">Soup of the day is <!--% todays_soup %--> !</a>
```

ie you are reserving the `config.` prefix for parameters you are expecting to come from the config. To set the defaults in this case you could do this:

```python

    defaults = {
        'config.soup_website_url' => 'http://www.example.com/soup-addicts',
        'config.some_other_url' => 'http://www.example.com/some-other-url'
    
        #...
    }

    nest.defaults( defaults )

```

but writing 'config.' repeatedly is a bit effortful, so Template-Nest allows you to do the following:


```html

    defaults = {

        'config': {

            'soup_website_url': 'http://www.example.com/soup-addicts',
            'some_other_url': 'http://www.example.com/some-other-url'
    
            #...
        },

        'some_other_namespace': {

            # other params?

        }

    }

    nest.defaults( defaults )
    nest.defaults_namespace_char('.') # not actually necessary, as '.' is the default

```

Now Template-Nest will replace `config.soup_website_url` with what it finds in

```python

    defaults[config][soup_website_url]

```

See `defaults_namespace_char`.



### defaults_namespace_char

Allows you to provide a "namespaced" defaults dict rather than just a flat one. ie instead of doing this:

```python

    nest.defaults({
        'variable1': 'value1',
        'variable2': 'value2',

        # ...

    })
```

You can do this:


```python

    nest.defaults({        
        'namespace1': {
            'variable1': 'value1',
            'variable2': 'value2'
        },

        'namespace2': {
            'variable1': 'value3',
            'variable2': 'value4
        }
    })
```

Specify your `defaults_namespace_char` to tell Template-Nest how to match these defaults in your template:

```python
    nest.defaults_namespace_char('-')
```

so now the token

```
    <% namespace1-variable1 %>
```

will be replaced with `value2`. Note the default `defaults_namespace_char` is a fullstop (period) character.


### error_on_bad_params

If you attempt to populate a template with a parameter that doesn't exist (ie the name is not found in the template) then this normally results in an error. This default behaviour is recommended in most circumstances as it guards against typos and sloppy code. However, there may be circumstances where you want processing to carry on regardless. In this case set `error_on_bad_params` to `False`:

```python
    nest.error_on_bad_params( False )
```

### escape_char

On rare occasions you may actually want to use the exact character string you are using for your token delimiters in one of your templates. e.g. say you are using token_delims `[%` and `%]`, and you have this in your template:

```
    Hello [% name %],

        did you know we are using token delimiters [% and %] in our templates?

    lots of love
    Roger
```

Clearly in this case we are a bit stuck because Template-Nest is going to think `[% and %]` is a token to be replaced. Not to worry, we can *escape* the opening token delimiter:

```
    Hello [% name %],

        did you know we are using token delimiters \[% and %] in our templates?

    lots of love
    Roger
```

In the output the backslash will be removed, and the `[% and %]` will get printed verbatim. 

`escape_char` is set to be a backslash by default. This means if you want an actual backslash to be printed, you would need a double backslash in your template.

You can change the escape character if necessary:

```python
    nest.escape_char('X')
```

or you can turn it off completely if you are confident you'll never want to escape anything. Do so by passing in the empty string to `escape_char`:

```python
    nest.escape_char('')
```


### fixed_indent

Intended to improve readability when inspecting nested templates. Consider the following example:

box.html:

```html
    <div class='box'>
        <!--% contents %-->
    </div>
```


photo.html:

```html
    <div>
        <img src='/some_image.jpg'>
    </div>
```

In the python:


```python
    nest = Nest({
        token_delims => ['<!--%','%-->']
    })
    
    nest.render({
        'NAME': 'box',
        'contents': 'image'
    })
```

Output:

```html
<div class='box'>
    <div>
    <img src='/some_image.jpg'>
</div>
</div>
```

Note the ugly indenting. In fact this is completely correct behaviour in terms of faithfully replacing the token 

```html
    <!--% contents %-->
```

with the `photo.html` template - the nested template starts exactly from where the token was placed, and each character is printed verbatim, including the new lines.

However, a lot of the time we really want output that looks like this:

```html
<div class='box'>
    <div>
        <image src='/some_image.jpg'>  # the indent is maintained
    </div>                             # for every line in the child
</div>                                 # template
```

To get this more readable output, then set `fixed_indent` to `True`:

```python
    nest.fixed_indent( True )
```

Bear in mind that this will result in extra space characters being inserted into the output.



### name_label

The default is `NAME` (all-caps, case-sensitive). Of course if `NAME` is interpreted as the filename of the template, then you can't use `NAME` as one of the variables in your template. ie

```
    <% NAME %>
```

will never get populated. If you really are adamant about needing to have a template variable called `NAME` - or you have some other reason for wanting an alternative label point to your template filename, then you can set name_label:

```python
    nest.name_label( 'MYLABEL' )

    #and now

    component = {
        'MYLABEL': 'name_of_my_component'
        #...
    }
```

### render

Convert a template structure to output text. Expects a dict (or list) containing dicts/lists/plain text.

e.g.

widget.html:

```html
    <div class='widget'>
        <h4>I am a widget</h4>
        <div>
            <!--% widget_body %-->
        </div>
    </div>
```


widget_body.html:
```html
    <div>
        <div>I am the widget body!</div>    
        <div><!--% some_widget_property %--></div>
    </div>
```

```python
    widget = {
        'NAME': 'widget',
        'widget_body': {
            'NAME': 'widget_body',
            'some_widget_property': 'Totally useless widget'
        }
    }

    print( nest.render( widget ) )
```

Output:

```html
    <div class='widget'>
        <h4>I am a widget</h4>
        <div>
            <div>
                <div>I am the widget body!</div>    
                <div>Totally useless widget</div>
            </div>
        </div>
    </div>
```


### show_labels

Get/set the show_labels property. This is a boolean with default `False`. Setting this to `True` results in adding comments to the output so you can identify which template output text came from. This is useful in development when you have many templates. E.g. adding 

```python
    nest.show_labels( True )
```

to the example in the synopsis results in the following:

```html
    <!-- BEGIN page -->
    <html>
        <head>
            <style>
                div { 
                    padding: 20px;
                    margin: 20px;
                    background-color: yellow;
                }
            </style>
        </head>

        <body>
            
    <!-- BEGIN box -->
    <div>
        First nested box
    </div>
    <!-- END box -->

    <!-- BEGIN box -->
    <div>
        Second nested box
    </div>
    <!-- END box -->

        </body>
    </html>
    <!-- END page -->
```

What if you're not templating html, and you still want labels? Then you should set `comment_delims` to whatever is appropriate for the thing you are templating.



### template_dir

Get/set the dir where Template-Nest looks for your templates. E.g.

```python
    nest.template_dir( '/my/template/dir' )
```

Now if I have

```python
    component = {
        NAME => 'hello',
        #...
    }
```

and `template_ext = '.html'`, we'll expect to find the template at `/my/template/dir/hello.html`.


Note that if you have some kind of directory structure for your templates (ie they are not all in the same directory), you can do something like this:

```python
    component = {
        'NAME': '/my/component/location',
        'contents': 'some contents or other'
    }
```

Template-Nest will then prepend `NAME` with `template_dir`, append `template_ext` and look in that location for the file. So in our example if `template_dir = '/my/template/dir'` and `template_ext = '.html'` then the template file will be expected to exist at `/my/template/dir/my/component/location.html`.

Of course if you want components to be nested arbitrarily, it might not make sense to contain them in a prescriptive directory structure. 


### template_ext

Get/set the template extension. This is so you can save typing your template extension all the time if it's always the same. The default is `.html` - however, there is no reason why this templating system could not be used to construct any other type of file (or why you could not use another extension even if you were producing html). So e.g. if you are wanting to manipulate javascript files:

```python
    nest.template_ext('.js')

    # then

    js_file = {
        'NAME': 'some_js_file'
        #...
    }
```

So here Template-Nest will look in `template_dir` for `some_js_file.js`.

If you don't want to specify a particular `template_ext` (presumably because files don't all have the same extension) - then you can do

```python
    nest.template_ext('')
```

In this case you would need to have NAME point to the full filename. ie

```python
    nest.template_ext('')

    component = {
        NAME => 'hello.html',
        #...
    }
```


### token_delims

Get/set the delimiters that define a token (to be replaced). `token_delims` is a 2 element list - corresponding to the opening and closing delimiters. For example

```python
    nest.token_delims( ['[%', '%]'] )
```

would mean that Template-Nest would now recognise and interpolate tokens in the format

```
    [% token_name %]
```

The default token_delims are the mason style delimiters `<%` and `%>`. Note that for `HTML` the token delimiters `<!--%` and `%-->` make a lot of sense, since they allow raw templates (ie that have not had values filled in) to render as good `HTML`.


## Building a template-less platform with Template-Nest

Recently someone reviewing Template-Nest suggested it wasn't a good system because "you end up with thousands of tiny templates". After some consideration I realised not only is this claim incorrect, the truth is pretty much the opposite: while you do end up with small templates (surely a good thing), you don't end up with more of them. In fact, you ought to end up with substantially less.

This is because once you've created the smallest units you expect to repeat, you then collect those together to create larger units - and so on. In other words you create a tree structure, which will tend to have the smallest repeating units at the bottom (the actual templates). You are in fact creating your pages with the minimal amount of repetition.

At this point I began to wonder what you would end up with if you took this philosophy to its extreme. In other words you start with the smallest possible building blocks imaginable, and build your pages from there. The result is quite interesting. I am not sure if it is a purely academic exercise for now, as I haven't tried to build it. However, so far I've been able to think of a response to every objection I could dream up. So it remains for someone to tell me why they think the scheme I am about to propose is not a good idea.

It goes like this: you can build any html page with the following 3 "templates":

* "standalone":

```
<[% tag %][% attributes %]>
```

* "closing":

```
<[% tag %][% attributes %]>[% contents %]</[% tag %]>
```


* "attribute":

```
 [% key %]="[% value %]"
```

(note the single space character at the beginning of the `attribute` template.)

The main purpose of coming up with this was as a "riducto ad absurdum" argument to respond to the "thousands of templates" claim: its clear from this that the finer-grained you make your templates, the *less* of them you need.

Then I started wondering if this is isn't just an academic idea, but would actually work practically, and might even be a considerably superior method of rendering html?

The templates are so small, they barely qualify as templates. It would be just as easy to stick them in constants in your code (given html itself is not likely to change any time soon). Hence this is why I referred to this system as "template-less". We go down to such tiny granularity that we end up with repeating units that might as well just be supplied directly by code.

Ridiculous, you think? Actually, due to the "tree effect" phenomenon I already mentioned, it seems really quite quick to get to page-sized output. Consider this:

```python
def css_tag( href ):

    return nest.render({
        'NAME': 'standalone',
        'tag': 'link',
        'attributes': [{
            'NAME': 'attribute'
            'key': 'href',
            'value': href
        }, {
            'NAME': 'attribute'
            'key': 'href',
            'value': href
        }]
    })


def script_tag( href ):

    return nest.render({
        'NAME': 'closing',
        'tag': 'script',
        'attributes': [{
            'NAME': 'attribute',
            'key': 'type',
            'value': 'text/javascript'
        }, {
            'NAME': 'attribute',
            'key': 'src',
            'value': href
        }
    })


def section_container( contents ):
    return nest.render({
        'NAME': 'closing',
        'tag': 'div',
        'attributes': {
            'NAME': 'attribute',
            'key': 'class',
            'value': 'section'
        },
        'contents': contents
    })
)

def page_header( title ):

    return nest.render({
        'NAME': 'closing',
        'tag': 'header',
        'contents': [
            css_tag('/css/local.css'),
            css_tag('/css/third_party.css'),
            script_tag(/js/local.js'),
            script_tag(/js/third_party.js'),
            { 'NAME': 'closing',
              'contents': title
            }   
        ]
    })
    
def page( title,contents,footer ):

    return nest.render([
        page_header(title),
        {
            'NAME': 'closing',
            'tag': 'body',
            'contents': [{
                section_container( contents ),
                section_container( footer )
            }]
        }
    ])
 
 # etc...
```


So in this scheme you have functions that hand you the individual tags. Then functions that call those functions... and so on. Pretty quickly you have functions which produce much larger scale content. (In fact, doesn't the size of output increase exponentially with each nested function call? Say your first function produces a single tag, and the second invokes a set of those tags. The third produces a set of sets. The fourth...)

What you've really done is swap out flat relatively immutable text files for dynamic, modifiable functions. Take for example the `script_tag` function above. That function is now going to get called for every single script tag on the page. Want to change `text/javascript` to something else? You can do it in a second in our template-less system. Can you do that with large flat templates? It's going to be a major search and replace job.

Actually you can intervene and make modifications at any point in the tree structure, with a change made only in one place, so that no more or less than the desired elements are affected. It is DRY taken to it's logical conclusion.

### Objections?

1. Overhead

    The main objection that immediately sprung to my mind is processing overhead. "Surely you don't seriously want to build large pages by individually rendering each and every single element? Those bottom level functions are going to get called an insane number of times!"

    That's true, but what about if we introduce caching? Suppose we create some kind of wrapper around those functions to return a cached value if we've seen the input before? So for example, the first time you call `css_tag` with `href = "example.com/css/my.css"` it actually performs the render, but the second time it finds the value corresponding to `example.com/css/my.css` in the cache, and delivers the chunk of html directly? That cuts the function call chain short, and delivers the html without hitting the lower level functions at all. Actually, isn't this fantastically efficient? Now you're only going to render those specific chunks you've never seen before. 

    (Ok - I guess there are going to be limits to how much you can cache, but still...)

2. "You end up with a lot of functions!"

    I don't actually think this is going to be any kind of issue, but I'm trying to imagine what an objector might say. Yes, I think you'll have more functions - you'll probably have an extra module or so full of those low level functions that deliver individual tags. But so what?

3. "It's difficult to visualise page output."

    If you like looking at files in a text editor, then this is true. However, it would be quite easy to have some kind of test system which meant you could call any individual function and look at the output. Potentially you could have it render in "debug" mode so it inserted comments saying which function each chunk came from (similar to Template-Nest's `show_comments` method.

4. ...?

    I don't know! Tell me why this wouldn't work? If you can't, maybe I'll try and build it...


## COPYRIGHT AND LICENSE

Copyright &copy; 2019 by Tom Gracey

This library is free software; you can redistribute it and/or modify
it under the MIT License.

