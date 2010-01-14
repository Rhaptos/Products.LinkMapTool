LinkMapTool

  This Zope Product is part of the Rhaptos system
  (http://software.cnx.rice.edu)

  LinkMapTool provides a CMF tool for storing extra links between an
  object and other objects or an a link from an object to an external
  site.  These links are stored on the tool and not on the object.

  This is somewhat similar to Archetypes' References, but better
  integrated with Rhaptos, particularly the versioning system of
  RhaptosRepository.

  Link endpoints are specified via a path, so LinkMapTool is only
  viable for content objects whose path isn't goin to change (like
  objects in the RhaptosRepository).


Future plans

  - Perhaps integrate with RhaptosRepository ?

  - Could/Should this be implemented with Archetypes References?

  - Extensible metadata for links
