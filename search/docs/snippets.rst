Snippets
========

You can build a snippet for you search results. Rest API described in the :doc:`rest-api` documentation.
In this part describes the main idea.

When you has setuped search index you can apply snippet for search results. Use rest API to manage snippets.
Snippet has structure and rules:

    * {"index_name": ", snippet(text_field_name, '{match}') as __text_field_name"}
    * index_name - name of search index for snippet will applied.
    * text_field_name - name of text field for snippet.
    * match - leave as is. Internal variable.
    * __text_field_name - output snippet field name, should be equal to text_field_name and starts with `__`.


