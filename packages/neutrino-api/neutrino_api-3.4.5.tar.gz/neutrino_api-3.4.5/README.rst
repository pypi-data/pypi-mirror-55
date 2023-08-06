Getting started
===============

The general-purpose API

Initialization
--------------

Authentication
~~~~~~~~~~~~~~

In order to setup authentication and initialization of the API client,
you need the following information.

+-------------+----------------+
| Parameter   | Description    |
+=============+================+
| user\_id    | Your user ID   |
+-------------+----------------+
| api\_key    | Your API key   |
+-------------+----------------+

API client can be initialized as following.

.. code:: python

    # Configuration parameters and credentials
    user_id = 'user_id' # Your user ID
    api_key = 'api_key' # Your API key

    client = NeutrinoApiClient(user_id, api_key)

Class Reference
===============

List of Controllers
-------------------

-  `Imaging <#imaging>`__
-  `Telephony <#telephony>`__
-  `DataTools <#data_tools>`__
-  `SecurityAndNetworking <#security_and_networking>`__
-  `Geolocation <#geolocation>`__
-  `ECommerce <#e_commerce>`__
-  `WWW <#www>`__

\ |Class:| Imaging
------------------

Get controller instance
~~~~~~~~~~~~~~~~~~~~~~~

An instance of the ``Imaging`` class can be accessed from the API
Client.

.. code:: python

     imaging_controller = client.imaging

\ |Method:| image\_resize
~~~~~~~~~~~~~~~~~~~~~~~~~

    Resize an image and output as either JPEG or PNG. See:
    https://www.neutrinoapi.com/api/image-resize/

.. code:: python

    def image_resize(self,
                         image_url,
                         width,
                         height,
                         format='png')

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| imageUrl     | ``Requi | The URL to the |
|              | red``   | source image   |
+--------------+---------+----------------+
| width        | ``Requi | The width to   |
|              | red``   | resize to (in  |
|              |         | px) while      |
|              |         | preserving     |
|              |         | aspect ratio   |
+--------------+---------+----------------+
| height       | ``Requi | The height to  |
|              | red``   | resize to (in  |
|              |         | px) while      |
|              |         | preserving     |
|              |         | aspect ratio   |
+--------------+---------+----------------+
| format       | ``Optio | The output     |
|              | nal``   | image format,  |
|              | ``Defau | can be either  |
|              | ltValue | png or jpg     |
|              | ``      |                |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    image_url = 'image-url'
    width = 189
    height = 189
    format = 'png'

    result = imaging_controller.image_resize(image_url, width, height, format)

\ |Method:| qr\_code
~~~~~~~~~~~~~~~~~~~~

    Generate a QR code as a PNG image. See:
    https://www.neutrinoapi.com/api/qr-code/

.. code:: python

    def qr_code(self,
                    content,
                    width=256,
                    height=256,
                    fg_color='#000000',
                    bg_color='#ffffff')

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| content      | ``Requi | The content to |
|              | red``   | encode into    |
|              |         | the QR code    |
|              |         | (e.g. a URL or |
|              |         | a phone        |
|              |         | number)        |
+--------------+---------+----------------+
| width        | ``Optio | The width of   |
|              | nal``   | the QR code    |
|              | ``Defau | (in px)        |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| height       | ``Optio | The height of  |
|              | nal``   | the QR code    |
|              | ``Defau | (in px)        |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| fgColor      | ``Optio | The QR code    |
|              | nal``   | foreground     |
|              | ``Defau | color          |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| bgColor      | ``Optio | The QR code    |
|              | nal``   | background     |
|              | ``Defau | color          |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    content = 'content'
    width = 256
    height = 256
    fg_color = '#000000'
    bg_color = '#ffffff'

    result = imaging_controller.qr_code(content, width, height, fg_color, bg_color)

\ |Method:| image\_watermark
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Watermark one image with another image. See:
    https://www.neutrinoapi.com/api/image-watermark/

.. code:: python

    def image_watermark(self,
                            image_url,
                            watermark_url,
                            opacity=50,
                            format='png',
                            position='center',
                            width=None,
                            height=None)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| imageUrl     | ``Requi | The URL to the |
|              | red``   | source image   |
+--------------+---------+----------------+
| watermarkUrl | ``Requi | The URL to the |
|              | red``   | watermark      |
|              |         | image          |
+--------------+---------+----------------+
| opacity      | ``Optio | The opacity of |
|              | nal``   | the watermark  |
|              | ``Defau | (0 to 100)     |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| format       | ``Optio | The output     |
|              | nal``   | image format,  |
|              | ``Defau | can be either  |
|              | ltValue | png or jpg     |
|              | ``      |                |
+--------------+---------+----------------+
| position     | ``Optio | The position   |
|              | nal``   | of the         |
|              | ``Defau | watermark      |
|              | ltValue | image,         |
|              | ``      | possible       |
|              |         | values are:    |
|              |         | center,        |
|              |         | top-left,      |
|              |         | top-center,    |
|              |         | top-right,     |
|              |         | bottom-left,   |
|              |         | bottom-center, |
|              |         | bottom-right   |
+--------------+---------+----------------+
| width        | ``Optio | If set resize  |
|              | nal``   | the resulting  |
|              |         | image to this  |
|              |         | width (in px)  |
|              |         | while          |
|              |         | preserving     |
|              |         | aspect ratio   |
+--------------+---------+----------------+
| height       | ``Optio | If set resize  |
|              | nal``   | the resulting  |
|              |         | image to this  |
|              |         | height (in px) |
|              |         | while          |
|              |         | preserving     |
|              |         | aspect ratio   |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    image_url = 'image-url'
    watermark_url = 'watermark-url'
    opacity = 50
    format = 'png'
    position = 'center'
    width = 189
    height = 189

    result = imaging_controller.image_watermark(image_url, watermark_url, opacity, format, position, width, height)

\ |Method:| html\_5\_render
~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Render HTML content to PDF, JPG or PNG. See:
    https://www.neutrinoapi.com/api/html5-render/

.. code:: python

    def html_5_render(self,
                          content,
                          format='PDF',
                          page_size='A4',
                          title=None,
                          margin=0,
                          margin_left=0,
                          margin_right=0,
                          margin_top=0,
                          margin_bottom=0,
                          landscape=False,
                          zoom=1,
                          grayscale=False,
                          media_print=False,
                          media_queries=False,
                          forms=False,
                          css=None,
                          image_width=1024,
                          image_height=None,
                          render_delay=0,
                          header_text_left=None,
                          header_text_center=None,
                          header_text_right=None,
                          header_size=9,
                          header_font='Courier',
                          header_font_size=11,
                          header_line=False,
                          footer_text_left=None,
                          footer_text_center=None,
                          footer_text_right=None,
                          footer_size=9,
                          footer_font='Courier',
                          footer_font_size=11,
                          footer_line=False,
                          page_width=None,
                          page_height=None)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| content      | ``Requi | The HTML       |
|              | red``   | content. This  |
|              |         | can be either  |
|              |         | a URL to load  |
|              |         | HTML from or   |
|              |         | an actual HTML |
|              |         | content string |
+--------------+---------+----------------+
| format       | ``Optio | Which format   |
|              | nal``   | to output,     |
|              | ``Defau | available      |
|              | ltValue | options are:   |
|              | ``      | PDF, PNG, JPG  |
+--------------+---------+----------------+
| pageSize     | ``Optio | Set the        |
|              | nal``   | document page  |
|              | ``Defau | size, can be   |
|              | ltValue | one of: A0 -   |
|              | ``      | A9, B0 - B10,  |
|              |         | Comm10E, DLE   |
|              |         | or Letter      |
+--------------+---------+----------------+
| title        | ``Optio | The document   |
|              | nal``   | title          |
+--------------+---------+----------------+
| margin       | ``Optio | The document   |
|              | nal``   | margin (in mm) |
|              | ``Defau |                |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| marginLeft   | ``Optio | The document   |
|              | nal``   | left margin    |
|              | ``Defau | (in mm)        |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| marginRight  | ``Optio | The document   |
|              | nal``   | right margin   |
|              | ``Defau | (in mm)        |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| marginTop    | ``Optio | The document   |
|              | nal``   | top margin (in |
|              | ``Defau | mm)            |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| marginBottom | ``Optio | The document   |
|              | nal``   | bottom margin  |
|              | ``Defau | (in mm)        |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| landscape    | ``Optio | Set the        |
|              | nal``   | document to    |
|              | ``Defau | lanscape       |
|              | ltValue | orientation    |
|              | ``      |                |
+--------------+---------+----------------+
| zoom         | ``Optio | Set the zoom   |
|              | nal``   | factor when    |
|              | ``Defau | rendering the  |
|              | ltValue | page (2.0 for  |
|              | ``      | double size,   |
|              |         | 0.5 for half   |
|              |         | size)          |
+--------------+---------+----------------+
| grayscale    | ``Optio | Render the     |
|              | nal``   | final document |
|              | ``Defau | in grayscale   |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| mediaPrint   | ``Optio | Use @media     |
|              | nal``   | print CSS      |
|              | ``Defau | styles to      |
|              | ltValue | render the     |
|              | ``      | document       |
+--------------+---------+----------------+
| mediaQueries | ``Optio | Activate all   |
|              | nal``   | @media queries |
|              | ``Defau | before         |
|              | ltValue | rendering.     |
|              | ``      | This can be    |
|              |         | useful if you  |
|              |         | wan't to       |
|              |         | render the     |
|              |         | mobile version |
|              |         | of a           |
|              |         | responsive     |
|              |         | website        |
+--------------+---------+----------------+
| forms        | ``Optio | Generate real  |
|              | nal``   | (fillable) PDF |
|              | ``Defau | forms from     |
|              | ltValue | HTML forms     |
|              | ``      |                |
+--------------+---------+----------------+
| css          | ``Optio | Inject custom  |
|              | nal``   | CSS into the   |
|              |         | HTML. e.g.     |
|              |         | 'body {        |
|              |         | background-col |
|              |         | or:            |
|              |         | red;}'         |
+--------------+---------+----------------+
| imageWidth   | ``Optio | If rendering   |
|              | nal``   | to an image    |
|              | ``Defau | format (PNG or |
|              | ltValue | JPG) use this  |
|              | ``      | image width    |
|              |         | (in pixels)    |
+--------------+---------+----------------+
| imageHeight  | ``Optio | If rendering   |
|              | nal``   | to an image    |
|              |         | format (PNG or |
|              |         | JPG) use this  |
|              |         | image height   |
|              |         | (in pixels).   |
|              |         | The default is |
|              |         | automatic      |
|              |         | which          |
|              |         | dynamically    |
|              |         | sets the image |
|              |         | height based   |
|              |         | on the content |
+--------------+---------+----------------+
| renderDelay  | ``Optio | Number of      |
|              | nal``   | milliseconds   |
|              | ``Defau | to wait before |
|              | ltValue | rendering the  |
|              | ``      | page (can be   |
|              |         | useful for     |
|              |         | pages with     |
|              |         | animations     |
|              |         | etc)           |
+--------------+---------+----------------+
| headerTextLe | ``Optio | Text to print  |
| ft           | nal``   | to the         |
|              |         | left-hand side |
|              |         | header of each |
|              |         | page. e.g. 'My |
|              |         | header - Page  |
|              |         | {page\_number} |
|              |         | of             |
|              |         | {total\_pages} |
|              |         | '              |
+--------------+---------+----------------+
| headerTextCe | ``Optio | Text to print  |
| nter         | nal``   | to the center  |
|              |         | header of each |
|              |         | page           |
+--------------+---------+----------------+
| headerTextRi | ``Optio | Text to print  |
| ght          | nal``   | to the         |
|              |         | right-hand     |
|              |         | side header of |
|              |         | each page      |
+--------------+---------+----------------+
| headerSize   | ``Optio | The height of  |
|              | nal``   | your header    |
|              | ``Defau | (in mm)        |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| headerFont   | ``Optio | Set the header |
|              | nal``   | font. Fonts    |
|              | ``Defau | available:     |
|              | ltValue | Times,         |
|              | ``      | Courier,       |
|              |         | Helvetica,     |
|              |         | Arial          |
+--------------+---------+----------------+
| headerFontSi | ``Optio | Set the header |
| ze           | nal``   | font size (in  |
|              | ``Defau | pt)            |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| headerLine   | ``Optio | Draw a full    |
|              | nal``   | page width     |
|              | ``Defau | horizontal     |
|              | ltValue | line under     |
|              | ``      | your header    |
+--------------+---------+----------------+
| footerTextLe | ``Optio | Text to print  |
| ft           | nal``   | to the         |
|              |         | left-hand side |
|              |         | footer of each |
|              |         | page. e.g. 'My |
|              |         | footer - Page  |
|              |         | {page\_number} |
|              |         | of             |
|              |         | {total\_pages} |
|              |         | '              |
+--------------+---------+----------------+
| footerTextCe | ``Optio | Text to print  |
| nter         | nal``   | to the center  |
|              |         | header of each |
|              |         | page           |
+--------------+---------+----------------+
| footerTextRi | ``Optio | Text to print  |
| ght          | nal``   | to the         |
|              |         | right-hand     |
|              |         | side header of |
|              |         | each page      |
+--------------+---------+----------------+
| footerSize   | ``Optio | The height of  |
|              | nal``   | your footer    |
|              | ``Defau | (in mm)        |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| footerFont   | ``Optio | Set the footer |
|              | nal``   | font. Fonts    |
|              | ``Defau | available:     |
|              | ltValue | Times,         |
|              | ``      | Courier,       |
|              |         | Helvetica,     |
|              |         | Arial          |
+--------------+---------+----------------+
| footerFontSi | ``Optio | Set the footer |
| ze           | nal``   | font size (in  |
|              | ``Defau | pt)            |
|              | ltValue |                |
|              | ``      |                |
+--------------+---------+----------------+
| footerLine   | ``Optio | Draw a full    |
|              | nal``   | page width     |
|              | ``Defau | horizontal     |
|              | ltValue | line above     |
|              | ``      | your footer    |
+--------------+---------+----------------+
| pageWidth    | ``Optio | Set the PDF    |
|              | nal``   | page width     |
|              |         | explicitly (in |
|              |         | mm)            |
+--------------+---------+----------------+
| pageHeight   | ``Optio | Set the PDF    |
|              | nal``   | page height    |
|              |         | explicitly (in |
|              |         | mm)            |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    content = 'content'
    format = 'PDF'
    page_size = 'A4'
    title = 'title'
    margin = 0
    margin_left = 0
    margin_right = 0
    margin_top = 0
    margin_bottom = 0
    landscape = False
    zoom = 1
    grayscale = False
    media_print = False
    media_queries = False
    forms = False
    css = 'css'
    image_width = 1024
    image_height = 189
    render_delay = 0
    header_text_left = 'header-text-left'
    header_text_center = 'header-text-center'
    header_text_right = 'header-text-right'
    header_size = 9
    header_font = 'Courier'
    header_font_size = 11
    header_line = False
    footer_text_left = 'footer-text-left'
    footer_text_center = 'footer-text-center'
    footer_text_right = 'footer-text-right'
    footer_size = 9
    footer_font = 'Courier'
    footer_font_size = 11
    footer_line = False
    page_width = 189
    page_height = 189

    result = imaging_controller.html_5_render(content, format, page_size, title, margin, margin_left, margin_right, margin_top, margin_bottom, landscape, zoom, grayscale, media_print, media_queries, forms, css, image_width, image_height, render_delay, header_text_left, header_text_center, header_text_right, header_size, header_font, header_font_size, header_line, footer_text_left, footer_text_center, footer_text_right, footer_size, footer_font, footer_font_size, footer_line, page_width, page_height)

`Back to List of Controllers <#list_of_controllers>`__

\ |Class:| Telephony
--------------------

Get controller instance
~~~~~~~~~~~~~~~~~~~~~~~

An instance of the ``Telephony`` class can be accessed from the API
Client.

.. code:: python

     telephony_controller = client.telephony

\ |Method:| verify\_security\_code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Check if a security code from one of the verify APIs is valid. See:
    https://www.neutrinoapi.com/api/verify-security-code/

.. code:: python

    def verify_security_code(self,
                                 security_code)

Parameters
^^^^^^^^^^

+----------------+----------------+-------------------------------+
| Parameter      | Tags           | Description                   |
+================+================+===============================+
| securityCode   | ``Required``   | The security code to verify   |
+----------------+----------------+-------------------------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    security_code = 'security-code'

    result = telephony_controller.verify_security_code(security_code)

\ |Method:| hlr\_lookup
~~~~~~~~~~~~~~~~~~~~~~~

    Connect to the global mobile cellular network and retrieve the
    status of a mobile device. See:
    https://www.neutrinoapi.com/api/hlr-lookup/

.. code:: python

    def hlr_lookup(self,
                       number,
                       country_code=None)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| number       | ``Requi | A phone number |
|              | red``   |                |
+--------------+---------+----------------+
| countryCode  | ``Optio | ISO 2-letter   |
|              | nal``   | country code,  |
|              |         | assume numbers |
|              |         | are based in   |
|              |         | this country.  |
|              |         | If not set     |
|              |         | numbers are    |
|              |         | assumed to be  |
|              |         | in             |
|              |         | international  |
|              |         | format (with   |
|              |         | or without the |
|              |         | leading +      |
|              |         | sign)          |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    number = 'number'
    country_code = 'country-code'

    result = telephony_controller.hlr_lookup(number, country_code)

\ |Method:| phone\_playback
~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Make an automated call to any valid phone number and playback an
    audio message. See: https://www.neutrinoapi.com/api/phone-playback/

.. code:: python

    def phone_playback(self,
                           number,
                           audio_url)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| number       | ``Requi | The phone      |
|              | red``   | number to      |
|              |         | call. Must be  |
|              |         | in valid       |
|              |         | international  |
|              |         | format         |
+--------------+---------+----------------+

\| audioUrl \| ``Required`` \| A URL to a valid audio file. Accepted
audio formats are:

.. raw:: html

   <ul>

.. raw:: html

   <li>

MP3

.. raw:: html

   </li>

.. raw:: html

   <li>

WAV

.. raw:: html

   </li>

.. raw:: html

   <li>

OGG

.. raw:: html

   </li>

.. raw:: html

   </ul>

You can use the following MP3 URL for testing:
https://www.neutrinoapi.com/test-files/test1.mp3 \|

Example Usage
^^^^^^^^^^^^^

.. code:: python

    number = 'number'
    audio_url = 'audio-url'

    result = telephony_controller.phone_playback(number, audio_url)

\ |Method:| sms\_verify
~~~~~~~~~~~~~~~~~~~~~~~

    Send a unique security code to any mobile device via SMS. See:
    https://www.neutrinoapi.com/api/sms-verify/

.. code:: python

    def sms_verify(self,
                       number,
                       code_length=5,
                       security_code=None,
                       country_code=None,
                       language_code='en')

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| number       | ``Requi | The phone      |
|              | red``   | number to send |
|              |         | a verification |
|              |         | code to        |
+--------------+---------+----------------+
| codeLength   | ``Optio | The number of  |
|              | nal``   | digits to use  |
|              | ``Defau | in the         |
|              | ltValue | security code  |
|              | ``      | (must be       |
|              |         | between 4 and  |
|              |         | 12)            |
+--------------+---------+----------------+
| securityCode | ``Optio | Pass in your   |
|              | nal``   | own security   |
|              |         | code. This is  |
|              |         | useful if you  |
|              |         | have           |
|              |         | implemented    |
|              |         | TOTP or        |
|              |         | similar 2FA    |
|              |         | methods. If    |
|              |         | not set then   |
|              |         | we will        |
|              |         | generate a     |
|              |         | secure random  |
|              |         | code           |
+--------------+---------+----------------+
| countryCode  | ``Optio | ISO 2-letter   |
|              | nal``   | country code,  |
|              |         | assume numbers |
|              |         | are based in   |
|              |         | this country.  |
|              |         | If not set     |
|              |         | numbers are    |
|              |         | assumed to be  |
|              |         | in             |
|              |         | international  |
|              |         | format (with   |
|              |         | or without the |
|              |         | leading +      |
|              |         | sign)          |
+--------------+---------+----------------+

\| languageCode \| ``Optional`` ``DefaultValue`` \| The language to send
the verification code in, available languages are:

.. raw:: html

   <ul>

.. raw:: html

   <li>

de - German

.. raw:: html

   </li>

.. raw:: html

   <li>

en - English

.. raw:: html

   </li>

.. raw:: html

   <li>

es - Spanish

.. raw:: html

   </li>

.. raw:: html

   <li>

fr - French

.. raw:: html

   </li>

.. raw:: html

   <li>

it - Italian

.. raw:: html

   </li>

.. raw:: html

   <li>

pt - Portuguese

.. raw:: html

   </li>

.. raw:: html

   <li>

ru - Russian

.. raw:: html

   </li>

.. raw:: html

   </ul>

\|

Example Usage
^^^^^^^^^^^^^

.. code:: python

    number = 'number'
    code_length = 5
    security_code = 189
    country_code = 'country-code'
    language_code = 'en'

    result = telephony_controller.sms_verify(number, code_length, security_code, country_code, language_code)

\ |Method:| sms\_message
~~~~~~~~~~~~~~~~~~~~~~~~

    Send a free-form message to any mobile device via SMS. See:
    https://www.neutrinoapi.com/api/sms-message/

.. code:: python

    def sms_message(self,
                        number,
                        message,
                        country_code=None)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| number       | ``Requi | The phone      |
|              | red``   | number to send |
|              |         | a message to   |
+--------------+---------+----------------+
| message      | ``Requi | The SMS        |
|              | red``   | message to     |
|              |         | send. Messages |
|              |         | are truncated  |
|              |         | to a maximum   |
|              |         | of 150         |
|              |         | characters for |
|              |         | ASCII content  |
|              |         | OR 70          |
|              |         | characters for |
|              |         | UTF content    |
+--------------+---------+----------------+
| countryCode  | ``Optio | ISO 2-letter   |
|              | nal``   | country code,  |
|              |         | assume numbers |
|              |         | are based in   |
|              |         | this country.  |
|              |         | If not set     |
|              |         | numbers are    |
|              |         | assumed to be  |
|              |         | in             |
|              |         | international  |
|              |         | format (with   |
|              |         | or without the |
|              |         | leading +      |
|              |         | sign)          |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    number = 'number'
    message = 'message'
    country_code = 'country-code'

    result = telephony_controller.sms_message(number, message, country_code)

\ |Method:| phone\_verify
~~~~~~~~~~~~~~~~~~~~~~~~~

    Make an automated call to any valid phone number and playback a
    unique security code. See:
    https://www.neutrinoapi.com/api/phone-verify/

.. code:: python

    def phone_verify(self,
                         number,
                         code_length=6,
                         security_code=None,
                         playback_delay=800,
                         country_code=None,
                         language_code='en')

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| number       | ``Requi | The phone      |
|              | red``   | number to send |
|              |         | the            |
|              |         | verification   |
|              |         | code to        |
+--------------+---------+----------------+
| codeLength   | ``Optio | The number of  |
|              | nal``   | digits to use  |
|              | ``Defau | in the         |
|              | ltValue | security code  |
|              | ``      | (between 4 and |
|              |         | 12)            |
+--------------+---------+----------------+
| securityCode | ``Optio | Pass in your   |
|              | nal``   | own security   |
|              |         | code. This is  |
|              |         | useful if you  |
|              |         | have           |
|              |         | implemented    |
|              |         | TOTP or        |
|              |         | similar 2FA    |
|              |         | methods. If    |
|              |         | not set then   |
|              |         | we will        |
|              |         | generate a     |
|              |         | secure random  |
|              |         | code           |
+--------------+---------+----------------+
| playbackDela | ``Optio | The delay in   |
| y            | nal``   | milliseconds   |
|              | ``Defau | between the    |
|              | ltValue | playback of    |
|              | ``      | each security  |
|              |         | code           |
+--------------+---------+----------------+
| countryCode  | ``Optio | ISO 2-letter   |
|              | nal``   | country code,  |
|              |         | assume numbers |
|              |         | are based in   |
|              |         | this country.  |
|              |         | If not set     |
|              |         | numbers are    |
|              |         | assumed to be  |
|              |         | in             |
|              |         | international  |
|              |         | format (with   |
|              |         | or without the |
|              |         | leading +      |
|              |         | sign)          |
+--------------+---------+----------------+

\| languageCode \| ``Optional`` ``DefaultValue`` \| The language to
playback the verification code in, available languages are:

.. raw:: html

   <ul>

.. raw:: html

   <li>

de - German

.. raw:: html

   </li>

.. raw:: html

   <li>

en - English

.. raw:: html

   </li>

.. raw:: html

   <li>

es - Spanish

.. raw:: html

   </li>

.. raw:: html

   <li>

fr - French

.. raw:: html

   </li>

.. raw:: html

   <li>

it - Italian

.. raw:: html

   </li>

.. raw:: html

   <li>

pt - Portuguese

.. raw:: html

   </li>

.. raw:: html

   <li>

ru - Russian

.. raw:: html

   </li>

.. raw:: html

   </ul>

\|

Example Usage
^^^^^^^^^^^^^

.. code:: python

    number = 'number'
    code_length = 6
    security_code = 189
    playback_delay = 800
    country_code = 'country-code'
    language_code = 'en'

    result = telephony_controller.phone_verify(number, code_length, security_code, playback_delay, country_code, language_code)

`Back to List of Controllers <#list_of_controllers>`__

\ |Class:| DataTools
--------------------

Get controller instance
~~~~~~~~~~~~~~~~~~~~~~~

An instance of the ``DataTools`` class can be accessed from the API
Client.

.. code:: python

     data_tools_controller = client.data_tools

\ |Method:| email\_validate
~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Parse, validate and clean an email address. See:
    https://www.neutrinoapi.com/api/email-validate/

.. code:: python

    def email_validate(self,
                           email,
                           fix_typos=False)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| email        | ``Requi | An email       |
|              | red``   | address        |
+--------------+---------+----------------+
| fixTypos     | ``Optio | Automatically  |
|              | nal``   | attempt to fix |
|              | ``Defau | typos in the   |
|              | ltValue | address        |
|              | ``      |                |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    email = 'email'
    fix_typos = False

    result = data_tools_controller.email_validate(email, fix_typos)

\ |Method:| user\_agent\_info
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Parse, validate and get detailed user-agent information from a user
    agent string. See: https://www.neutrinoapi.com/api/user-agent-info/

.. code:: python

    def user_agent_info(self,
                            user_agent)

Parameters
^^^^^^^^^^

+-------------+----------------+-----------------------+
| Parameter   | Tags           | Description           |
+=============+================+=======================+
| userAgent   | ``Required``   | A user agent string   |
+-------------+----------------+-----------------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    user_agent = 'user-agent'

    result = data_tools_controller.user_agent_info(user_agent)

\ |Method:| bad\_word\_filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Detect bad words, swear words and profanity in a given text. See:
    https://www.neutrinoapi.com/api/bad-word-filter/

.. code:: python

    def bad_word_filter(self,
                            content,
                            censor_character=None)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| content      | ``Requi | The content to |
|              | red``   | scan. This can |
|              |         | be either a    |
|              |         | URL to load    |
|              |         | content from   |
|              |         | or an actual   |
|              |         | content string |
+--------------+---------+----------------+
| censorCharac | ``Optio | The character  |
| ter          | nal``   | to use to      |
|              |         | censor out the |
|              |         | bad words      |
|              |         | found          |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    content = 'content'
    censor_character = 'censor-character'

    result = data_tools_controller.bad_word_filter(content, censor_character)

\ |Method:| convert
~~~~~~~~~~~~~~~~~~~

    A powerful unit conversion tool. See:
    https://www.neutrinoapi.com/api/convert/

.. code:: python

    def convert(self,
                    from_value,
                    from_type,
                    to_type)

Parameters
^^^^^^^^^^

+-------------+----------------+----------------------------------------------------+
| Parameter   | Tags           | Description                                        |
+=============+================+====================================================+
| fromValue   | ``Required``   | The value to convert from (e.g. 10.95)             |
+-------------+----------------+----------------------------------------------------+
| fromType    | ``Required``   | The type of the value to convert from (e.g. USD)   |
+-------------+----------------+----------------------------------------------------+
| toType      | ``Required``   | The type to convert to (e.g. EUR)                  |
+-------------+----------------+----------------------------------------------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    from_value = 'from-value'
    from_type = 'from-type'
    to_type = 'to-type'

    result = data_tools_controller.convert(from_value, from_type, to_type)

\ |Method:| phone\_validate
~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Parse, validate and get location information about a phone number.
    See: https://www.neutrinoapi.com/api/phone-validate/

.. code:: python

    def phone_validate(self,
                           number,
                           country_code=None,
                           ip=None)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| number       | ``Requi | A phone        |
|              | red``   | number. This   |
|              |         | can be in      |
|              |         | international  |
|              |         | format (E.164) |
|              |         | or local       |
|              |         | format. If     |
|              |         | passing local  |
|              |         | format you     |
|              |         | should use the |
|              |         | 'country-code' |
|              |         | or 'ip'        |
|              |         | options as     |
|              |         | well           |
+--------------+---------+----------------+
| countryCode  | ``Optio | ISO 2-letter   |
|              | nal``   | country code,  |
|              |         | assume numbers |
|              |         | are based in   |
|              |         | this country.  |
|              |         | If not set     |
|              |         | numbers are    |
|              |         | assumed to be  |
|              |         | in             |
|              |         | international  |
|              |         | format (with   |
|              |         | or without the |
|              |         | leading +      |
|              |         | sign)          |
+--------------+---------+----------------+
| ip           | ``Optio | Pass in a      |
|              | nal``   | users IP       |
|              |         | address and we |
|              |         | will assume    |
|              |         | numbers are    |
|              |         | based in the   |
|              |         | country of the |
|              |         | IP address     |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    number = 'number'
    country_code = 'country-code'
    ip = 'ip'

    result = data_tools_controller.phone_validate(number, country_code, ip)

`Back to List of Controllers <#list_of_controllers>`__

\ |Class:| SecurityAndNetworking
--------------------------------

Get controller instance
~~~~~~~~~~~~~~~~~~~~~~~

An instance of the ``SecurityAndNetworking`` class can be accessed from
the API Client.

.. code:: python

     security_and_networking_controller = client.security_and_networking

\ |Method:| ip\_probe
~~~~~~~~~~~~~~~~~~~~~

    Analyze and extract provider information for an IP address. See:
    https://www.neutrinoapi.com/api/ip-probe/

.. code:: python

    def ip_probe(self,
                     ip)

Parameters
^^^^^^^^^^

+-------------+----------------+------------------------+
| Parameter   | Tags           | Description            |
+=============+================+========================+
| ip          | ``Required``   | IPv4 or IPv6 address   |
+-------------+----------------+------------------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    ip = 'ip'

    result = security_and_networking_controller.ip_probe(ip)

\ |Method:| email\_verify
~~~~~~~~~~~~~~~~~~~~~~~~~

    SMTP based email address verification. See:
    https://www.neutrinoapi.com/api/email-verify/

.. code:: python

    def email_verify(self,
                         email,
                         fix_typos=False)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| email        | ``Requi | An email       |
|              | red``   | address        |
+--------------+---------+----------------+
| fixTypos     | ``Optio | Automatically  |
|              | nal``   | attempt to fix |
|              | ``Defau | typos in the   |
|              | ltValue | address        |
|              | ``      |                |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    email = 'email'
    fix_typos = False

    result = security_and_networking_controller.email_verify(email, fix_typos)

\ |Method:| ip\_blocklist
~~~~~~~~~~~~~~~~~~~~~~~~~

    The IP Blocklist API will detect potentially malicious or dangerous
    IP addresses. See: https://www.neutrinoapi.com/api/ip-blocklist/

.. code:: python

    def ip_blocklist(self,
                         ip)

Parameters
^^^^^^^^^^

+-------------+----------------+---------------------------+
| Parameter   | Tags           | Description               |
+=============+================+===========================+
| ip          | ``Required``   | An IPv4 or IPv6 address   |
+-------------+----------------+---------------------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    ip = 'ip'

    result = security_and_networking_controller.ip_blocklist(ip)

\ |Method:| host\_reputation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Check the reputation of an IP address, domain name, FQDN or URL
    against a comprehensive list of blacklists and blocklists. See:
    https://www.neutrinoapi.com/api/host-reputation/

.. code:: python

    def host_reputation(self,
                            host,
                            list_rating=3)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| host         | ``Requi | An IP address, |
|              | red``   | domain name,   |
|              |         | FQDN or URL.   |
|              |         | If you supply  |
|              |         | a domain/URL   |
|              |         | it will be     |
|              |         | checked        |
|              |         | against the    |
|              |         | URI DNSBL      |
|              |         | lists          |
+--------------+---------+----------------+
| listRating   | ``Optio | Only check     |
|              | nal``   | lists with     |
|              | ``Defau | this rating or |
|              | ltValue | better         |
|              | ``      |                |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    host = 'host'
    list_rating = 3

    result = security_and_networking_controller.host_reputation(host, list_rating)

`Back to List of Controllers <#list_of_controllers>`__

\ |Class:| Geolocation
----------------------

Get controller instance
~~~~~~~~~~~~~~~~~~~~~~~

An instance of the ``Geolocation`` class can be accessed from the API
Client.

.. code:: python

     geolocation_controller = client.geolocation

\ |Method:| geocode\_reverse
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Convert a geographic coordinate (latitude and longitude) into a real
    world address. See: https://www.neutrinoapi.com/api/geocode-reverse/

.. code:: python

    def geocode_reverse(self,
                            latitude,
                            longitude,
                            language_code='en',
                            zoom='address')

Parameters
^^^^^^^^^^

+-------------+----------------+----------------------------------------------------+
| Parameter   | Tags           | Description                                        |
+=============+================+====================================================+
| latitude    | ``Required``   | The location latitude in decimal degrees format    |
+-------------+----------------+----------------------------------------------------+
| longitude   | ``Required``   | The location longitude in decimal degrees format   |
+-------------+----------------+----------------------------------------------------+

\| languageCode \| ``Optional`` ``DefaultValue`` \| The language to
display results in, available languages are:

.. raw:: html

   <ul>

.. raw:: html

   <li>

de, en, es, fr, it, pt, ru

.. raw:: html

   </li>

.. raw:: html

   </ul>

\| \| zoom \| ``Optional`` ``DefaultValue`` \| The zoom level to respond
with:

.. raw:: html

   <ul>

.. raw:: html

   <li>

address - the most precise address available

.. raw:: html

   </li>

.. raw:: html

   <li>

street - the street level

.. raw:: html

   </li>

.. raw:: html

   <li>

city - the city level

.. raw:: html

   </li>

.. raw:: html

   <li>

state - the state level

.. raw:: html

   </li>

.. raw:: html

   <li>

country - the country level

.. raw:: html

   </li>

.. raw:: html

   </ul>

\|

Example Usage
^^^^^^^^^^^^^

.. code:: python

    latitude = 'latitude'
    longitude = 'longitude'
    language_code = 'en'
    zoom = 'address'

    result = geolocation_controller.geocode_reverse(latitude, longitude, language_code, zoom)

\ |Method:| ip\_info
~~~~~~~~~~~~~~~~~~~~

    Get location information about an IP address and do reverse DNS
    (PTR) lookups. See: https://www.neutrinoapi.com/api/ip-info/

.. code:: python

    def ip_info(self,
                    ip,
                    reverse_lookup=False)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| ip           | ``Requi | IPv4 or IPv6   |
|              | red``   | address        |
+--------------+---------+----------------+
| reverseLooku | ``Optio | Do a reverse   |
| p            | nal``   | DNS (PTR)      |
|              | ``Defau | lookup. This   |
|              | ltValue | option can add |
|              | ``      | extra delay to |
|              |         | the request so |
|              |         | only use it if |
|              |         | you need it    |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    ip = 'ip'
    reverse_lookup = False

    result = geolocation_controller.ip_info(ip, reverse_lookup)

\ |Method:| geocode\_address
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Geocode an address, partial address or just the name of a place.
    See: https://www.neutrinoapi.com/api/geocode-address/

.. code:: python

    def geocode_address(self,
                            address,
                            country_code=None,
                            language_code='en',
                            fuzzy_search=False)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| address      | ``Requi | The address,   |
|              | red``   | partial        |
|              |         | address or     |
|              |         | name of a      |
|              |         | place to try   |
|              |         | and locate     |
+--------------+---------+----------------+
| countryCode  | ``Optio | The ISO        |
|              | nal``   | 2-letter       |
|              |         | country code   |
|              |         | to be biased   |
|              |         | towards (the   |
|              |         | default is no  |
|              |         | country bias)  |
+--------------+---------+----------------+

\| languageCode \| ``Optional`` ``DefaultValue`` \| The language to
display results in, available languages are:

.. raw:: html

   <ul>

.. raw:: html

   <li>

de, en, es, fr, it, pt, ru

.. raw:: html

   </li>

.. raw:: html

   </ul>

\| \| fuzzySearch \| ``Optional`` ``DefaultValue`` \| If no matches are
found for the given address, start performing a recursive fuzzy search
until a geolocation is found. This option is recommended for processing
user input or implementing auto-complete. We use a combination of
approximate string matching and data cleansing to find possible location
matches \|

Example Usage
^^^^^^^^^^^^^

.. code:: python

    address = 'address'
    country_code = 'country-code'
    language_code = 'en'
    fuzzy_search = False

    result = geolocation_controller.geocode_address(address, country_code, language_code, fuzzy_search)

`Back to List of Controllers <#list_of_controllers>`__

\ |Class:| ECommerce
--------------------

Get controller instance
~~~~~~~~~~~~~~~~~~~~~~~

An instance of the ``ECommerce`` class can be accessed from the API
Client.

.. code:: python

     e_commerce_controller = client.e_commerce

\ |Method:| bin\_lookup
~~~~~~~~~~~~~~~~~~~~~~~

    Perform a BIN (Bank Identification Number) or IIN (Issuer
    Identification Number) lookup. See:
    https://www.neutrinoapi.com/api/bin-lookup/

.. code:: python

    def bin_lookup(self,
                       bin_number,
                       customer_ip=None)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| binNumber    | ``Requi | The BIN or IIN |
|              | red``   | number (the    |
|              |         | first 6 digits |
|              |         | of a credit    |
|              |         | card number)   |
+--------------+---------+----------------+
| customerIp   | ``Optio | Pass in the    |
|              | nal``   | customers IP   |
|              |         | address and we |
|              |         | will return    |
|              |         | some extra     |
|              |         | information    |
|              |         | about them     |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    bin_number = 'bin-number'
    customer_ip = 'customer-ip'

    result = e_commerce_controller.bin_lookup(bin_number, customer_ip)

`Back to List of Controllers <#list_of_controllers>`__

\ |Class:| WWW
--------------

Get controller instance
~~~~~~~~~~~~~~~~~~~~~~~

An instance of the ``WWW`` class can be accessed from the API Client.

.. code:: python

     www_controller = client.www

\ |Method:| url\_info
~~~~~~~~~~~~~~~~~~~~~

    Parse, analyze and retrieve content from the supplied URL. See:
    https://www.neutrinoapi.com/api/url-info/

.. code:: python

    def url_info(self,
                     url,
                     fetch_content=False,
                     ignore_certificate_errors=False,
                     timeout=20)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| url          | ``Requi | The URL to     |
|              | red``   | probe          |
+--------------+---------+----------------+
| fetchContent | ``Optio | If this URL    |
|              | nal``   | responds with  |
|              | ``Defau | html, text,    |
|              | ltValue | json or xml    |
|              | ``      | then return    |
|              |         | the response.  |
|              |         | This option is |
|              |         | useful if you  |
|              |         | want to        |
|              |         | perform        |
|              |         | further        |
|              |         | processing on  |
|              |         | the URL        |
|              |         | content (e.g.  |
|              |         | with the HTML  |
|              |         | Extract or     |
|              |         | HTML Clean     |
|              |         | APIs)          |
+--------------+---------+----------------+
| ignoreCertif | ``Optio | Ignore any     |
| icateErrors  | nal``   | TLS/SSL        |
|              | ``Defau | certificate    |
|              | ltValue | errors and     |
|              | ``      | load the URL   |
|              |         | anyway         |
+--------------+---------+----------------+
| timeout      | ``Optio | Timeout in     |
|              | nal``   | seconds. Give  |
|              | ``Defau | up if still    |
|              | ltValue | trying to load |
|              | ``      | the URL after  |
|              |         | this number of |
|              |         | seconds        |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    url = 'url'
    fetch_content = False
    ignore_certificate_errors = False
    timeout = 20

    result = www_controller.url_info(url, fetch_content, ignore_certificate_errors, timeout)

\ |Method:| html\_clean
~~~~~~~~~~~~~~~~~~~~~~~

    Clean and sanitize untrusted HTML. See:
    https://www.neutrinoapi.com/api/html-clean/

.. code:: python

    def html_clean(self,
                       content,
                       output_type)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| content      | ``Requi | The HTML       |
|              | red``   | content. This  |
|              |         | can be either  |
|              |         | a URL to load  |
|              |         | HTML from or   |
|              |         | an actual HTML |
|              |         | content string |
+--------------+---------+----------------+
| outputType   | ``Requi | The level of   |
|              | red``   | sanitization,  |
|              |         | possible       |
|              |         | values are:    |
|              |         | plain-text:    |
|              |         | reduce the     |
|              |         | content to     |
|              |         | plain text     |
|              |         | only (no HTML  |
|              |         | tags at all)   |
|              |         | simple-text:   |
|              |         | allow only     |
|              |         | very basic     |
|              |         | text           |
|              |         | formatting     |
|              |         | tags like b,   |
|              |         | em, i, strong, |
|              |         | u basic-html:  |
|              |         | allow advanced |
|              |         | text           |
|              |         | formatting and |
|              |         | hyper links    |
|              |         | basic-html-wit |
|              |         | h-images:      |
|              |         | same as basic  |
|              |         | html but also  |
|              |         | allows image   |
|              |         | tags           |
|              |         | advanced-html: |
|              |         | same as basic  |
|              |         | html with      |
|              |         | images but     |
|              |         | also allows    |
|              |         | many more      |
|              |         | common HTML    |
|              |         | tags like      |
|              |         | table, ul, dl, |
|              |         | pre            |
+--------------+---------+----------------+

Example Usage
^^^^^^^^^^^^^

.. code:: python

    content = 'content'
    output_type = 'output-type'

    result = www_controller.html_clean(content, output_type)

\ |Method:| browser\_bot
~~~~~~~~~~~~~~~~~~~~~~~~

    Browser bot can extract content, interact with keyboard and mouse
    events, and execute JavaScript on a website. See:
    https://www.neutrinoapi.com/api/browser-bot/

.. code:: python

    def browser_bot(self,
                        url,
                        timeout=30,
                        delay=3,
                        selector=None,
                        mexec=None,
                        user_agent=None,
                        ignore_certificate_errors=False)

Parameters
^^^^^^^^^^

+--------------+---------+----------------+
| Parameter    | Tags    | Description    |
+==============+=========+================+
| url          | ``Requi | The URL to     |
|              | red``   | load           |
+--------------+---------+----------------+
| timeout      | ``Optio | Timeout in     |
|              | nal``   | seconds. Give  |
|              | ``Defau | up if still    |
|              | ltValue | trying to load |
|              | ``      | the page after |
|              |         | this number of |
|              |         | seconds        |
+--------------+---------+----------------+
| delay        | ``Optio | Delay in       |
|              | nal``   | seconds to     |
|              | ``Defau | wait before    |
|              | ltValue | capturing any  |
|              | ``      | page data,     |
|              |         | executing      |
|              |         | selectors or   |
|              |         | JavaScript     |
+--------------+---------+----------------+
| selector     | ``Optio | Extract        |
|              | nal``   | content from   |
|              |         | the page DOM   |
|              |         | using this     |
|              |         | selector.      |
|              |         | Commonly known |
|              |         | as a CSS       |
|              |         | selector, you  |
|              |         | can find a     |
|              |         | good reference |
|              |         | here           |
+--------------+---------+----------------+

\| mexec \| ``Optional`` ``Collection`` \| Execute JavaScript on the
page. Each array element should contain a valid JavaScript statement in
string form. If a statement returns any kind of value it will be
returned in the 'exec-results' response. For your convenience you can
also use the following special shortcut functions:

.. raw:: html

   <div>

sleep(seconds); Just wait/sleep for the specified number of seconds.
click('selector'); Click on the first element matching the given
selector. focus('selector'); Focus on the first element matching the
given selector. keys('characters'); Send the specified keyboard
characters. Use click() or focus() first to send keys to a specific
element. enter(); Send the Enter key. tab(); Send the Tab key.

.. raw:: html

   </div>

Example:

.. raw:: html

   <div>

[ "click('#button-id')", "sleep(1)", "click('.field-class')",
"keys('1234')", "enter()" ]

.. raw:: html

   </div>

\| \| userAgent \| ``Optional`` \| Override the browsers default
user-agent string with this one \| \| ignoreCertificateErrors \|
``Optional`` ``DefaultValue`` \| Ignore any TLS/SSL certificate errors
and load the page anyway \|

Example Usage
^^^^^^^^^^^^^

.. code:: python

    url = 'url'
    timeout = 30
    delay = 3
    selector = 'selector'
    mexec = ['exec']
    user_agent = 'user-agent'
    ignore_certificate_errors = False

    result = www_controller.browser_bot(url, timeout, delay, selector, mexec, user_agent, ignore_certificate_errors)

`Back to List of Controllers <#list_of_controllers>`__

.. |Class:| image:: https://apidocs.io/img/class.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Class:| image:: https://apidocs.io/img/class.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Class:| image:: https://apidocs.io/img/class.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Class:| image:: https://apidocs.io/img/class.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Class:| image:: https://apidocs.io/img/class.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Class:| image:: https://apidocs.io/img/class.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Class:| image:: https://apidocs.io/img/class.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png
.. |Method:| image:: https://apidocs.io/img/method.png

