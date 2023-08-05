################
CherryPy ASK SDK
################

Extending `Ask SDK <https://github.com/alexa/alexa-skills-kit-sdk-for-python>`_ to work with CherryPy.

Quick Start
-----------

Mandatory `warning` from the upstream ask-sdk for python.

.. warning::

    These features are currently in beta. You can view the source
    code in the
    `Ask Python Sdk <https://github.com/alexa/alexa-skills-kit-sdk-for-python>`_
    repo on GitHub. The interface might change when the features are released as
    stable.

If you already have a skill built using the ASK SDK skill builders, then you
only need to do the following to set this up in your CherryPy application:

.. code-block:: python

    import cherrypy
    import cherrypy_ask_sdk
    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()
    # Register all handlers, interceptors etc.
    # For eg : sb.add_request_handler(LaunchRequestHandler())

    # add the ask_sdk_skill tool in the global ``cherrypy.tools`` toolbox.
    # Passing the cherrypy.tools toolbox is the default, but passing it
    # explicitly just to make it more explicit.
    cherrypy_ask_sdk.add_in_toolbox(cherrypy.tools)

    if __name__ == '__main__':
        cherrypy.quickstart(
            config={
                '/': {
                    'tools.ask_sdk_skill.on': True,
                    'tools.ask_sdk_skill.skill': sb.create(),
                    'tools.ask_sdk_skill.verify_signature': True,
                    'tools.ask_sdk_skill.verify_timestamp': True
                }
            }
        )

Installation
------------

.. code-block::

   pip install cherrypy-ask-sdk


Features
--------

- Works as an extension on skills built using ASK SDK. No need to learn
  something new.

- Provides default request signature and request timestamp verification.

- Provides a way to register multiple skills in the tree.


.. note::

   This package was heavily inspired by the official Flask Ask SDK.
