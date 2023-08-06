Getting started using a YAML file
---------------------------------

Using a text editor you can define the YAML structure of your register map relatively easily. It gets a little easier
if you use an editor that understands YAML, such as `Notepad++ <https://notepad-plus-plus.org/>`_ or an IDE such as
`PyCharm <https://www.jetbrains.com/pycharm/>`_.

The example below shows a register map skeleton that defines some properties of the memory space, along with a summary
and description of the register map. The modules section is left blank for now.

In any register map you must have at least one module.

.. code-block:: yaml

   registerMap: {
     # A memorySpace is not optional
     memorySpace: {
       # but all the parameters are optional.
       # Default: 0x0
       baseAddress: 0x1000
       # Default: None
       pageSize: None
       # Default: 32
       addressBits: 48
       # Default: 8
       memoryUnitBits: 16
     }
     summary: 'A short summary of the register map'
     description: 'A longer description of the register map'
     modules: [
     ]
   }

When you are done and have saved your YAML data to a file, your YAML register map can be loaded into Python.

.. code-block:: python

   import registerMap
   myMap = registerMap.load( 'registermap.yml' )

Let's test that the register map properties are loaded as expected.

.. code-block:: python

   assert myMap.memory.addressBits == 48
   assert myMap.memory.memoryUnitBits == 16
   assert myMap.memory.baseAddress == 0x1000

Another way to quickly get started is to use the Python API to create a register map, export it to
YAML and then copy-paste the YAML structures you find to create your data.

.. code-block:: python

   import registerMap

   myMap = registerMap.RegisterMap()
   myMap.addModule( 'mymodule' )
   myRegister = myMap['modules'][ 'mymodule' ].addRegister( 'myregister' )
   myField = myRegister.addField( 'my-field', [2, 4] )

   registerMap.save('myMap.yml', myMap)

When you initially create a map this way, or whenever you save register map YAML from Python you
will notice a number of properties with an underscore ('_') prefix. These are included for
reference for a human reader but the values themselves are automatically calculated; you should not
modify them, but if you do, don't expect your modifications to persist as changes will be
overwritten the next time you same YAML from Python and they will never have any effect when loaded
into Python.


Creating a module
^^^^^^^^^^^^^^^^^

.. code-block:: yaml
   modules:
     - module:
         constraints: {}
         description: ''
         instances: 1
         name: mymodule
         registers: []
         summary: ''

The ``instances`` properties is used when you are creating a series module.


Creating a register
^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml
   registers:
   - register:
       bitFields:[]
       bitmap:
       - destination: '[0:2]'
         destinationId: mymodule.myregister.my-field,
         source: '[2:4]'
       constraints: {}
       description: ''
       global: false
       mode: rw
       name: myregister
       public: true
       summary: ''

The particularly complicated bit here is defining the bitmap; when using Python this is taken care
of to varying degrees by the Python API, depending on the complexity of your bit mapping. The bit
map maps the bits of a member field to the bits of the register. The ``destination`` bit range is
the bit indices of the field. The ``destinationId`` is the canonical ID of the field you are
mapping and the ``source`` is the bit range of the register.

In the example above, bits [0:2] of the bit field are mapped to bits [2:4] of the register.

The definition of the bit field itself is described in the next section.

The ``global`` property is always false for now. It is a placeholder for a
`global register feature <https://gitlab.com/registerMap/registerMap/issues/31>`_.


Creating a local field
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml
   bitFields:
   - field:
       description: ''
       name: my-field
       parent: mymodule.myregister
       resetValue: 0x0
       size: 3
       summary: ''

The ``parent`` property is required to identify the bit field as local to the register and not
global (see below).


Creating a global field
^^^^^^^^^^^^^^^^^^^^^^^

A global field means that you intend to take the bits of that field and distribute them across
multiple registers and modules. As a general rule a global field is not recommended at all for
various reasons, not the least of which is that it greatly complicates software required to read,
write and manage such "distributed" fields. It is supported here because hardware designers
sometimes find it necessary to jam field bits into obscure locations and so a register map
description should be able to accommodate this.

In YAML, a global field must have one and only one instantiation that defines the reset value and
size of the field. Subsequent declarations of the global field must only define which bits of the
register are being attached to. A global field must not define a ``parent`` property.

In the example below we have two modules each with a register associating with a global field. To
try and reduce the noise a bit, properties that don't relate to the global field configuration have
been dropped.

Notes:

  * The register ``m1.myregister`` has a local field ``my-field``. The destination bit mapping uses
    a "third level" canonical id to address the field; ``m1.myregister.my-field``
  * The register ``m1.myregister`` contains the definition of the global field ``my-global-field``
    in it's ``bitFields`` section, including the reset value and size.
  * The register ``m2.other_register`` ``bitFields`` section is empty because it has no local
    fields and is associating with the global field that has already been defined in
    ``m1.myregister``.
  * ``m2.other_register`` contain a bit mapping to the global field ``my-global-field``
  * The global field ``my-global-field`` is always referenced using a "first level" canonical ID
    (just it's name).


.. code-block:: yaml
    registerMap:
      modules:
      - module:
          name: m1
          registers:
          - register:
              bitFields:
              - field: {description: '', name: my-field, parent: mymodule.myregister,
                  resetValue: 0x0, size: 3, summary: ''}
              - field: {description: '', name: my-global-field, resetValue: 0x0, size: 6,
                  summary: ''}
              bitmap:
              - {destination: '[0:2]', destinationId: m1.myregister.my-field, source: '[2:4]'}
              - {destination: '[3:5]', destinationId: my-global-field, source: '[5:7]'}
              name: myregister
      - module:
          name: m2
          registers:
          - register:
              bitFields: []
              bitmap:
              - {destination: '[0:2]', destinationId: my-global-field, source: '[1:3]'}
              name: other_register
