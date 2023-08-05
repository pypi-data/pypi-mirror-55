"""
Installation of "django-ajax-selects":
- Use pip to install "django-ajax-selects" and dependencies.
- In settings.py:

    - add "ajax_select" to INSTALLED_APPS.
    - Add:

            # magically include jqueryUI/js/css
            AJAX_SELECT_BOOTSTRAP = True
            AJAX_SELECT_INLINES = 'inline'

- Touch your project's wsgi.py file to load the "ajax_select" application.
- Run "python manage.py collectstatic".

To add a new ajax select:
- Include the import for the model class you will be selecting from at the top of this file (put it in alphabetical order).
- In this file, make a new class that extends LookupParent for the model you want to lookup using AJAX-selects (It is OK to just copy one of the other ones here).  Place it in alphabetical order in the file.
- Modify the get_query() and get_objects() methods to reference the correct model, fields in that model.
- If django 1.6 or earlier, in settings.py, add a line for your new channel to the AJAX_LOOKUP_CHANNELS property, like this, for person:
    'person' : ('context.lookups', 'PersonLookup'),
- In admin.py, either add or edit a form attribute to include your channel, and to tell the admin which field to map to which AJAX lookup.  So, for example, in Article, there is the following line:

        form = make_ajax_form( Article_Subject, dict( person = 'person', ) )

    - This line says, for Article_Subject, when entering 'person' field, lookup using the 'person' AJAX lookup channel.
    - The field names are the names from the model class definition, and can be any type of relation.  Channel names are the @register decorator contents in this file, or if django <= 1.6, the keys in AJAX_LOOKUP_CHANNELS in your settings.py file.
    - So, If you were to add a lookup for organization, then you'd have:

            form = make_ajax_form( Article_Subject, dict( person = 'person', subject_organization = 'organization', ) )

- To use in a plain django Form, use `ajax_select.make_ajax_field` inside a ModelForm child, assigned to a variable named for the field you want to look up:

    - person  = make_ajax_field( Article_Subject, 'person', 'coding_person', help_text = None )
"""

# python imports
import logging

# django imports
from django.db.models import Q

# context imports
from context.models import Entity
from context.models import Entity_Relation_Type
from context.models import Entity_Type
from context.models import Term
from context.models import Trait_Type
from context.models import Vocabulary

# python_utilities - django_ajax_selects_lookup_helper
from python_utilities.django_utils.django_ajax_selects_lookup_helper import LookupParent

# ajax_select imports
from ajax_select import register, LookupChannel


#===============================================================================#
# Individual child Lookup classes
#===============================================================================#


@register( "entity" )
class EntityLookup( LookupParent ):

    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( EntityLookup, self ).__init__()
        
        # initialize variables
        self.my_class = Entity
        
    #-- END method __init__() --#

    def get_query( self, q, request ):

        """
        return a query set.  you also have access to request.user if needed
        """

        # return reference
        query_set_OUT = None

        # is the q a number and is it the ID of an entity?
        query_set_OUT = self.get_instance_query( q, request, self.my_class )

        # got anything back?
        if ( query_set_OUT is None ):

            # No exact match for q as ID.  Return search of text in contributor.
            query_set_OUT = self.my_class.objects.filter( Q( name__icontains = q ) | Q( details_json__icontains = q ) | Q( entity_identifier__uuid__icontains = q ) | Q( notes__icontains = q ) | Q( tags__name__icontains = q ) )
            #query_set_OUT = self.my_class.objects.filter( Q( name__icontains = q ) | Q( details_json__icontains = q ) | Q( notes__icontains = q ) | Q( tags__name__icontains = q ) )
            
        #-- END retrieval of query set when no ID match. --#

        return query_set_OUT

    #-- END method get_query --#


    def get_objects(self,ids):

        """
        given a list of ids, return the objects ordered as you would like them
            on the admin page.  This is for displaying the currently selected
            items (in the case of a ManyToMany field)
        """
        return self.my_class.objects.filter(pk__in=ids).order_by( 'entity_types_set__entity_type', 'name' )

    #-- END method get_objects --#

#-- END class EntityLookup --#


@register( "entity_relation_type" )
class Entity_Relation_TypeLookup( LookupParent ):

    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( Entity_Relation_TypeLookup, self ).__init__()
        
        # initialize variables
        self.my_class = Entity_Relation_Type
        
    #-- END method __init__() --#


    def get_query( self, q, request ):

        """
        return a query set.  you also have access to request.user if needed
        """

        # return reference
        query_set_OUT = None

        # is the q a number and is it the ID of an entity?
        query_set_OUT = self.get_instance_query( q, request, self.my_class )

        # got anything back?
        if ( query_set_OUT is None ):

            # No exact match for q as ID.  Return search of text in contributor.
            query_set_OUT = self.my_class.objects.filter( Q( slug__icontains = q ) | Q( name__icontains = q ) | Q( related_model__icontains = q ) | Q( description__icontains = q ) | Q( notes__icontains = q ) | Q( tags__name__icontains = q ) )
            
        #-- END retrieval of query set when no ID match. --#

        return query_set_OUT

    #-- END method get_query --#


    def get_objects(self,ids):

        """
        given a list of ids, return the objects ordered as you would like them
            on the admin page.  This is for displaying the currently selected
            items (in the case of a ManyToMany field)
        """
        return self.my_class.objects.filter(pk__in=ids).order_by( 'slug' )

    #-- END method get_objects --#

#-- END class Entity_Relation_TypeLookup --#


@register( "entity_type" )
class Entity_TypeLookup( LookupParent ):

    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( Entity_TypeLookup, self ).__init__()
        
        # initialize variables
        self.my_class = Entity_Type
        
    #-- END method __init__() --#


    def get_query( self, q, request ):

        """
        return a query set.  you also have access to request.user if needed
        """

        # return reference
        query_set_OUT = None

        # is the q a number and is it the ID of an entity?
        query_set_OUT = self.get_instance_query( q, request, self.my_class )

        # got anything back?
        if ( query_set_OUT is None ):

            # No exact match for q as ID.  Return search of text in contributor.
            query_set_OUT = self.my_class.objects.filter( Q( slug__icontains = q ) | Q( name__icontains = q ) | Q( related_model__icontains = q ) | Q( description__icontains = q ) | Q( notes__icontains = q ) | Q( tags__name__icontains = q ) )
            
        #-- END retrieval of query set when no ID match. --#

        return query_set_OUT

    #-- END method get_query --#


    def get_objects(self,ids):

        """
        given a list of ids, return the objects ordered as you would like them
            on the admin page.  This is for displaying the currently selected
            items (in the case of a ManyToMany field)
        """
        return self.my_class.objects.filter(pk__in=ids).order_by( 'slug' )

    #-- END method get_objects --#

#-- END class Entity_TypeLookup --#


@register( "term" )
class TermLookup( LookupParent ):

    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( TermLookup, self ).__init__()
        
        # initialize variables
        self.my_class = Term
        
    #-- END method __init__() --#

    def get_query( self, q, request ):

        """
        return a query set.  you also have access to request.user if needed
        """

        # return reference
        query_set_OUT = None

        # is the q a number and is it the ID of an article?
        query_set_OUT = self.get_instance_query( q, request, self.my_class )

        # got anything back?
        if ( query_set_OUT is None ):

            # No exact match for q as ID.  Return search of text in contributor.
            query_set_OUT = self.my_class.objects.filter( Q( value__icontains = q ) | Q( label__icontains = q ) | Q( description__icontains = q ) | Q( notes__icontains = q ) | Q( tags__name__icontains = q ) )

        #-- END retrieval of query set when no ID match. --#

        return query_set_OUT

    #-- END method get_query --#


    def get_objects(self,ids):

        """
        given a list of ids, return the objects ordered as you would like them
            on the admin page.  This is for displaying the currently selected
            items (in the case of a ManyToMany field)
        """
        return self.my_class.objects.filter(pk__in=ids).order_by( 'vocabulary', 'value' )

    #-- END method get_objects --#

#-- END class TermLookup --#


@register( "trait_type" )
class Trait_TypeLookup( LookupParent ):

    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( Trait_TypeLookup, self ).__init__()
        
        # initialize variables
        self.my_class = Trait_Type
        
    #-- END method __init__() --#


    def get_query( self, q, request ):

        """
        return a query set.  you also have access to request.user if needed
        """

        # return reference
        query_set_OUT = None

        # is the q a number and is it the ID of an article?
        query_set_OUT = self.get_instance_query( q, request, self.my_class )

        # got anything back?
        if ( query_set_OUT is None ):

            # No exact match for q as ID.  Return search of text in contributor.
            query_set_OUT = self.my_class.objects.filter( Q( name__icontains = q ) | Q( slug__icontains = q ) | Q( related_model__icontains = q ) | Q( description__icontains = q ) | Q( notes__icontains = q ) | Q( vocabulary__name__icontains = q ) | Q( tags__name__icontains = q ) )

        #-- END retrieval of query set when no ID match. --#

        return query_set_OUT

    #-- END method get_query --#


    def get_objects(self,ids):

        """
        given a list of ids, return the objects ordered as you would like them
            on the admin page.  This is for displaying the currently selected
            items (in the case of a ManyToMany field)
        """
        return self.my_class.objects.filter(pk__in=ids).order_by( 'slug' )

    #-- END method get_objects --#

#-- END class Trait_TypeLookup --#


@register( "vocabulary" )
class VocabularyLookup( LookupParent ):

    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( VocabularyLookup, self ).__init__()
        
        # initialize variables
        self.my_class = Vocabulary
        
    #-- END method __init__() --#

    def get_query( self, q, request ):

        """
        return a query set.  you also have access to request.user if needed
        """

        # return reference
        query_set_OUT = None

        # is the q a number and is it the ID of an article?
        query_set_OUT = self.get_instance_query( q, request, self.my_class )

        # got anything back?
        if ( query_set_OUT is None ):

            # No exact match for q as ID.  Return search of text in contributor.
            query_set_OUT = self.my_class.objects.filter( Q( name__icontains = q ) | Q( description__icontains = q ) | Q( notes__icontains = q ) | Q( tags__name__icontains = q ) )

        #-- END retrieval of query set when no ID match. --#

        return query_set_OUT

    #-- END method get_query --#


    def get_objects(self,ids):

        """
        given a list of ids, return the objects ordered as you would like them
            on the admin page.  This is for displaying the currently selected
            items (in the case of a ManyToMany field)
        """
        return self.my_class.objects.filter(pk__in=ids).order_by( 'name' )

    #-- END method get_objects --#

#-- END class VocabularyLookup --#

