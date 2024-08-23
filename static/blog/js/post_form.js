document.addEventListener('DOMContentLoaded', function() {
  // Select2 initialization for tags
  $('#{{ form.tags.id_for_label }}').select2({
      tags: true,
      tokenSeparators: [',', ' '],
      placeholder: "Enter tags",
  });
});

