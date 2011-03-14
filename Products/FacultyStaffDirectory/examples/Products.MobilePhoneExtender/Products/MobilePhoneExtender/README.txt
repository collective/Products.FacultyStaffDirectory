MobilePhoneExtender

Versions

  For Plone 3 and up.

Dependencies

  * "FacultyStaffDirectory":http://plone.org/products/faculty-staff-directory/ 2.x
  
  * archetypes.schemaextender 1.x

Description
  
  You can add fields to the FacultyStaffDirectory content types by writing
  "extender" products. MobilePhoneExtender is an example one which
  adds a Mobile Phone field to Person objects (on the Contact Information tab).
  
  You can extrapolate from this example to make your own extenders:
  
  1. Make a copy of MobilePhoneExtender, and rename the folders to reflect the
     product name of your choice. For example, if you're writing a product to
     add a Favorite Color field to the Person type, you might call it
     FacultyStaffDirectoryFavoriteColor, call the egg
     Products.FacultyStaffDirectoryFavoriteColor and the folder inside the
     Products folder FacultyStaffDirectoryFavoriteColor. This naming convention
     makes your extender appear near FacultyStaffDirectory in alphabetical
     listings, making people more likely to find it.
  
  2. Replace all occurrences of "MobilePhoneExtender" in your new
     product with "FacultyStaffDirectoryFavoriteColor" (or whatever you called
     it).
  
  3. Customize the '_fields' list in the person.py file to add Favorite Color
     instead of Mobile Phone. Note that any fields you add must be of a type
     that subclasses 'ExtensionField'. See '_StringExtensionField' in person.py
     for an example.
  
  4. Test your extender. It should work at this point.
  
  Modifying Other Content Types
  
      To add fields to a content type other than Person, have your extender
      class (e.g. 'PersonExtender') adapt something other than 'IPerson' (and
      call them something else so as not to be misleading). For example, to
      extend Department, adapt 'IDepartment'. All the extensible interfaces are
      defined in FacultyStaffDirectory.interfaces. (You can also extend types
      that don't define an interface for you: just apply your own interface via
      ZCML. However, that's outside the scope of this document.)
  
  Showing Fields on View Templates
      
      In a future release, our view templates will be made out of viewlets,
      which you'll be able to replace piecemeal. Until then, you'll have to
      override the entire view template for whatever content type (or types) you
      extend. For example, if you add a field to Person, you'll need to include
      a person_view.pt with your product and do the usual skin registration
      dance upon product installation. MobilePhoneExtender doesn't
      demonstrate this at the moment, so the Mobile Phone field won't appear
      when viewing a Person, only when editing.

Installing the Example Extender

  1. Install FacultyStaffDirectory according to its README.txt.
  
  2. Place the MobilePhoneExtender folder in the Products folder, or use typical
     egg installation practice.
  
  3. Restart Zope.
  
  4. If you're using Plone 3 or later, go to your-plone-site &rarr; site setup
     &rarr; Add/Remove Products, and install MobilePhoneExtender.
    
Using the Example Extender
    
  1. In your Faculty/Staff Directory object, add a Person.
  
  2. Click the Person's Edit tab, and navigate to the Contact Information
     section. You should see a Mobile Phone field. Tada!

Version History

  ' ' 3.0 -- ' '

        * Switch to a IBrowserLayerAwareExtender

        * Modernize code (proper metadata for GS profiles, zcml registration of profiles, etc.)

        * Drop Plone 2.5 support.  

  ' ' 2.1 -- ' '
    
        * Added support for full i18n.
    
        * Added Spanish, French, Italian, Portugues, Türkçe localization.
    
        * Added a bash script which helps to update news strings for translation for l10n.
    
        * Added egg packaging, since it's nice to declare a dependency on
          archetypes.schemaextender.
        
        * Renamed from FacultyStaffDirectoryExtender to MobilePhoneExtender to
          make it clearer that this is an example name and should be changed.
          Lots of people never renamed their products.
  
  ' ' 2.0 -- Rewrote to work with FacultyStaffDirectory 2.0's new extension
             mechanism and vastly improved this README.
  
  ' ' 1.0.1 -- Minor documentation tweaks
  
  ' ' 1.0 -- Initial release

Authorship

  This product was developed by the WebLion group at Penn State.
  
  Many thanks to those who worked on archetypes.schemaextender.

Support

  * Please report bugs to support@weblion.psu.edu

  * More documentation:https://weblion.psu.edu/trac/weblion/wiki/FacultyStaffDirectory

  * Contact us::

    WebLion Project Team
    Penn State University
    304 The 300 Building
    University Park, PA 16802
    support@weblion.psu.edu
    814-863-4574

License

    Copyright (c) 2006-2011 The Pennsylvania State University. WebLion is
    developed and maintained by the WebLion Project Team, its partners, and
    members of the Penn State Zope Users Group.

    This program is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation; either version 2 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
    more details.

    You should have received a copy of the GNU General Public License along with
    this program; if not, write to the Free Software Foundation, Inc., 59 Temple
    Place, Suite 330, Boston, MA 02111-1307 USA.

    This document is written using the Structured Text format for conversion
    into alternative formats.
