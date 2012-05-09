var adjustFancybox, avatarUploadDone, get_open_options, photoUploadDone, resizePhoto;

window.origin_title = document.title;

$.cookie = function(name, value, options) {
  var cookie, cookieValue, cookies, date, domain, expires, path, secure, _i, _len;
  if (typeof value !== 'undefined') {
    options = options || {};
    if (value === null) {
      value = "";
      options.expires = -1;
    }
    expires = "";
    if (options.expires && (typeof options.expires === 'number' || options.expires.toUTCString)) {
      if (typeof options.expires === "number") {
        date = new Date;
        date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
      } else {
        date = options.expires;
      }
      expires = "; expires=" + (date.toUTCString());
    }
    path = options.path ? "; path=" + options.path : "";
    domain = options.domain ? "; domain=" + options.domain : "";
    secure = options.secure ? "; secure=" + options.secure : "";
    return document.cookie = [name, "=", encodeURIComponent(value), expires, path, domain, secure].join("");
  } else {
    cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      cookies = document.cookie.split(";");
      for (_i = 0, _len = cookies.length; _i < _len; _i++) {
        cookie = cookies[_i];
        cookie = jQuery.trim(cookie);
        if (cookie.substring(0, name.length + 1) === ("" + name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
};

photoUploadDone = function(result) {
  var $btn, key, val, _ref, _results;
  if (result.status === 'ok') {
    if (result.content.location) return window.location = result.content.location;
  } else {
    $btn = $('#photo-upload').find('.disabled');
    $btn.removeClass('disabled').val($btn.data('origin_text'));
    $('.error').hide();
    _ref = result.content;
    _results = [];
    for (key in _ref) {
      val = _ref[key];
      _results.push($("#" + key + "-error").html(val).show());
    }
    return _results;
  }
};

avatarUploadDone = function(result) {
  var $form, $submit_btn, key, val, _ref, _results;
  $form = $('#avatar-upload');
  $form.find('.success').hide();
  $submit_btn = $form.find('input[type="submit"]');
  $submit_btn.removeClass('disabled').val($submit_btn.data('origin_text'));
  if (result.status === 'ok') {
    $form.find('.avatar img').attr('src', result.content.avatar_url);
    return $form.find('.success').show();
  } else {
    $('.error').hide();
    _ref = result.content;
    _results = [];
    for (key in _ref) {
      val = _ref[key];
      _results.push($("#" + key + "-error").html(val).show());
    }
    return _results;
  }
};

resizePhoto = function(container_width, container_height, photo_width, photo_height) {
  var height_ratio, resized_photo_height, resized_photo_width, width_ratio;
  width_ratio = photo_width / container_width;
  height_ratio = photo_height / container_height;
  resized_photo_width = photo_width;
  resized_photo_height = photo_height;
  if (width_ratio > height_ratio && photo_width > container_width) {
    resized_photo_width = container_width;
    resized_photo_height = photo_height / width_ratio;
  } else if (height_ratio > width_ratio && photo_height > container_height) {
    resized_photo_height = container_height;
    resized_photo_width = photo_width / height_ratio;
  }
  return [parseInt(resized_photo_width), parseInt(resized_photo_height)];
};

adjustFancybox = function(photo_width, photo_height) {
  var $item, container_height, container_width, current, photo_extra_width, resized_photo_height, resized_photo_width, _ref;
  if (photo_width == null) photo_width = 0;
  if (photo_height == null) photo_height = 0;
  if (!photo_width) {
    current = $.fancybox.current;
    $item = $(current.element);
    photo_width = $item.data('photo-width');
    photo_height = $item.data('photo-height');
    if (!photo_width && (typeof meta_photo !== "undefined" && meta_photo !== null)) {
      photo_width = meta_photo.width;
      photo_height = meta_photo.height;
    }
  }
  if (photo_width) {
    photo_extra_width = $('#photo-extra').width() === 0 ? 0 : $('#photo-extra').innerWidth();
    container_width = $('.fancybox-outer').width() - photo_extra_width;
    container_height = $('.fancybox-outer').height();
    _ref = resizePhoto(container_width, container_height, photo_width, photo_height), resized_photo_width = _ref[0], resized_photo_height = _ref[1];
    $('#photo img').css({
      width: resized_photo_width + 'px',
      height: resized_photo_height + 'px',
      'margin-left': '-' + parseInt(resized_photo_width / 2) + 'px',
      'margin-top': '-' + parseInt(resized_photo_height / 2) + 'px',
      display: 'block'
    });
    $('#photo').css({
      width: container_width,
      height: container_height
    });
    $('#photo .left, #photo .right').css({
      width: parseInt(container_width / 2),
      height: container_height
    });
    return $('#photo-extra').css('height', ($('.fancybox-inner').height() - 30) + 'px');
  }
};

get_open_options = function(opts) {
  var defaults;
  if (opts == null) opts = {};
  defaults = {
    type: 'ajax',
    autoSize: false,
    width: '90%',
    height: '90%',
    padding: 0,
    scrolling: 'none',
    openEffect: 'none',
    closeEffect: 'none',
    closeClick: false,
    nextEffect: 'none',
    prevEffect: 'none',
    afterShow: function() {
      var $item;
      if ($.cookie('photofullsize')) {
        $('#photo-extra').hide().width(0);
        $('#photo .toggle-fullsize').addClass('icon-resize-small');
      }
      $item = $($.fancybox.current.element);
      if (opts.photo_width != null) {
        adjustFancybox(opts.photo_width, opts.photo_height);
      } else {
        adjustFancybox();
      }
      if (History.enabled && !$.browser.msie) {
        window.opening_fancybox = true;
        History.pushState({
          content: $('.fancybox-inner').html(),
          type: 'fancybox',
          index: $.fancybox.current.index
        }, $item.data('title'), $item.data('url'));
        return window.opening_fancybox = false;
      }
    },
    beforeShow: function() {
      return $('#photo img').hide();
    },
    onUpdate: function() {
      if (opts.photo_width != null) {
        return adjustFancybox(opts.photo_width, opts.photo_height);
      } else {
        return adjustFancybox();
      }
    },
    afterClose: function(current) {
      if (History.enabled && !$.browser.msie) {
        return History.pushState({}, window.origin_title, window.origin_location);
      }
    }
  };
  $.extend(defaults, opts);
  return defaults;
};

$.fn.photoToggleSidebarIcon = function() {
  return this.on('click', function(e) {
    $(this).next().toggle();
    return $(this).find('i').toggleClass('icon-slidedown');
  });
};

$.fn.photoLike = function() {
  return this.on('click', function(e) {
    var $icon, $this;
    e.preventDefault();
    $this = $(this);
    $icon = $this.find('i');
    return $.post($this.data('url'), function(data) {
      var $like_count, current_count;
      $like_count = $this.next().find('.like-count');
      if (data.status === 'ok') {
        if ($icon.hasClass('icon-liked-btn')) {
          $icon.removeClass('icon-liked-btn').addClass('icon-like-btn');
          current_count = parseInt($like_count.text());
          return $like_count.text(current_count - 1);
        } else {
          $icon.removeClass('icon-like-btn').addClass('icon-liked-btn');
          current_count = parseInt($like_count.text());
          return $like_count.text(current_count + 1);
        }
      }
    });
  });
};

$.fn.photoPrev = function() {
  return this.on('mouseover', function(e) {
    $(this).next().fadeIn('fast');
    return $(this).next().next().next().fadeOut('fast');
  }).on('mouseout', function(e) {
    return $(this).next().fadeOut('fast');
  }).on('click', function(e) {
    return $.fancybox.prev();
  });
};

$.fn.photoNext = function() {
  return this.on('mouseover', function(e) {
    $(this).next().fadeIn('fast');
    return $(this).prev().fadeOut('fast');
  }).on('mouseout', function(e) {
    return $(this).next().fadeOut('fast');
  }).on('click', function(e) {
    return $.fancybox.next();
  });
};

$.fn.photoCommentAdd = function() {
  return this.on('submit', function(e) {
    var $this;
    e.preventDefault();
    $this = $(this);
    return $.post($this.attr('action'), $this.serialize(), function(result) {
      if (result.status === 'ok') {
        $('#comment-create input[type="text"]').val('');
        return $('#comment-create').before(result.content.content);
      }
    });
  });
};

$.fn.photoCommentHover = function() {
  return this.on('mouseover', '.comment', function(e) {
    return $(this).find('a.close').show();
  }).on('mouseout', '.comment', function(e) {
    return $(this).find('a.close').hide();
  }).on('click', '.comment a.close', function(e) {
    var $this;
    e.preventDefault();
    $this = $(this);
    return $.post($this.attr('href'), function(result) {
      var $comment;
      if (result.status === 'ok') {
        $comment = $this.parent().parent().parent();
        $comment.next().fadeOut();
        return $comment.fadeOut();
      }
    });
  });
};

$.fn.photoContentEdit = function() {
  return this.on('click', function(e) {
    var $parent;
    $parent = $(this).parent().parent();
    $parent.hide();
    return $parent.next().show();
  });
};

$.fn.photoContentCancelEdit = function() {
  return this.on('click', function(e) {
    var $parent;
    $parent = $(this).parent().parent().parent();
    $parent.hide();
    return $parent.prev().show();
  });
};

$.fn.photoContentSubmit = function() {
  return this.on('submit', function(e) {
    var $submit_btn, $this;
    e.preventDefault();
    $this = $(this);
    $submit_btn = $this.find('input[type="submit"]');
    return $.post($this.attr('action'), $this.serialize(), function(result) {
      $submit_btn.removeClass('disabled').val($submit_btn.data('origin_text'));
      if (result.status === 'ok') {
        $('#photo-content h3 span').text($this.find('input[name="title"]').val());
        $('#photo-content .content').html($this.find('textarea[name="content"]').val());
        $this.parent().hide();
        return $this.parent().prev().show();
      }
    });
  });
};

$.fn.photoTagHover = function() {
  return this.on('mouseover', 'li', function(e) {
    return $(this).find('.close').css('visibility', 'visible');
  }).on('mouseout', 'li', function(e) {
    return $(this).find('.close').css('visibility', 'hidden');
  });
};

$.fn.photoTagAdd = function() {
  return this.on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).parent().hide();
    return $('#tagadd').show();
  });
};

$.fn.photoTagAddCancel = function() {
  return this.on('click', function(e) {
    e.preventDefault();
    $(this).parent().parent().hide();
    return $('#addtag').show();
  });
};

$.fn.photoTagAddSubmit = function() {
  return this.on('submit', function(e) {
    var $submit_btn, $this;
    e.preventDefault();
    $this = $(this);
    $submit_btn = $this.find('input[type="submit"]');
    return $.post($this.attr('action'), $this.serialize(), function(result) {
      var tag, _i, _len, _ref, _results;
      $submit_btn.removeClass('disabled').val($submit_btn.data('origin_text'));
      if (result.status === 'ok') {
        _ref = result.content.tags;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          tag = _ref[_i];
          _results.push($('#tags').append("                        <li><i class='icon-tag'></i> <a href='/tag/" + tag + "'>" + tag + "</a>                        <span class='close invisible'>×</span></li>"));
        }
        return _results;
      }
    });
  });
};

$.fn.photoTagClose = function() {
  return this.on('click', function(e) {
    var $this;
    e.preventDefault();
    $this = $(this);
    return $.post($this.data('url'), function(result) {
      if (result.status === 'ok') return $this.parent().fadeOut();
    }, 'json');
  });
};

$.fn.photoDelete = function() {
  return this.on('click', function(e) {
    return $(this).hide().next().show();
  });
};

$.fn.photoDeleteCancel = function() {
  return this.on('click', function(e) {
    e.preventDefault();
    return $(this).parent().hide().prev().show();
  });
};

$.fn.photoToggleFullsize = function() {
  return this.on('click', function(e) {
    var $this;
    $this = $(this);
    $this.toggleClass('icon-resize-small');
    if ($this.hasClass('icon-resize-small')) {
      $('#photo-extra').width(0);
      $('#photo-extra').hide();
      $.cookie('photofullsize', 1);
    } else {
      $('#photo-extra').width(285);
      $('#photo-extra').show();
      $.cookie('photofullsize', '');
    }
    return adjustFancybox();
  });
};

$.fn.photoDeleteSubmit = function() {
  return this.on('click', function(e) {
    var $this;
    e.preventDefault();
    $this = $(this);
    return $.post($this.data('url'), function(result) {
      if (result.status === 'ok') return window.location = result.content.location;
    }, 'json');
  });
};

$.fn.ajaxSubmit = function() {
  return this.on('submit', function(e) {
    var $submit_btn, $this;
    $this = $(this);
    $submit_btn = $this.find('input[type="submit"]');
    $this.find('.error').hide();
    $this.find('.success').hide();
    e.preventDefault();
    return $.post($this.attr('action'), $this.serialize(), function(result) {
      var key, val, _ref, _results;
      $submit_btn.removeClass('disabled').val($submit_btn.data('origin_text'));
      if (result.status === 'ok') {
        if (result.content.location != null) {
          return window.location = result.content.location;
        } else {
          return $this.find('.success').show();
        }
      } else {
        _ref = result.content;
        _results = [];
        for (key in _ref) {
          val = _ref[key];
          _results.push($("#" + key + "-error").html(val).show());
        }
        return _results;
      }
    }, 'json');
  });
};

$.fn.userFollow = function() {
  return this.on('click', function(e) {
    var $btn, url;
    $btn = $(this);
    url = $btn.data('url');
    return $.post(url, function(data) {
      if (data.status === 'ok') {
        $btn.toggleClass('primary-btn');
        return $btn.text($btn.text() === '取消关注' ? '关注' : '取消关注');
      }
    });
  });
};

$.fn.photosFancy = function() {
  return this.on('click', function(e) {
    e.preventDefault();
    window.origin_location = location.href;
    return $.fancybox.open($('#photos a.fancybox'), get_open_options({
      index: $(this).data('index')
    }));
  });
};

$(function() {
  $('#sidebar .item').length && (function() {
    $('#sidebar .item').each(function(index) {
      return $(this).attr('vid', "item-" + index);
    });
    return $('#sidebar').on('click', '.item', function(e) {
      var $this, url, vid;
      e.preventDefault();
      $this = $(this);
      if (History.enabled && !$.browser.msie) {
        if ($this.hasClass('disabled')) return;
        $('.item').removeClass('highlight');
        $this.addClass('highlight');
        url = $this.data('url');
        vid = $this.attr('vid');
        return $.get(url, function(data) {
          History.pushState({
            content: data,
            vid: vid,
            type: 'sidebar_item'
          }, $this.data('title'), url);
          return $('#main').html(data);
        });
      } else {
        return window.location = $this.data('url');
      }
    });
  })();
  $('input.btn').live('click', function(e) {
    var $this;
    $this = $(this);
    if ($this.hasClass('disabled')) return false;
    $this.data('origin_text', $this.val());
    $this.addClass('disabled');
    $this.val('working...');
    return true;
  });
  if (History.enabled && !$.browser.msie && $('#main').html()) {
    History.pushState({
      type: 'sidebar_item',
      content: $('#main').html(),
      vid: 'nonexists'
    }, document.title, location.pathname + location.search);
    History.Adapter.bind(window, 'statechange', function() {
      var state;
      state = History.getState();
      if (!state.data) return;
      document.title = state.title;
      if (state.data.type !== 'fancybox') {
        $('#main').html(state.data.content);
        $.fancybox.close();
      }
      if (state.data.type === 'sidebar_item') {
        $('.item').removeClass('highlight');
        $("[vid=" + state.data.vid + "]").addClass('highlight');
      }
      if (state.data.type === 'fancybox') {
        if (!$('#main').html()) window.location.reload();
        if (!window.opening_fancybox) {
          if (!$.fancybox.isOpen) {
            $.fancybox.open($('#photos a.fancybox'), get_open_options());
          }
          $.fancybox.jumpto(state.data.index);
          return adjustFancybox();
        }
      }
    });
  }
  if (History.enabled && !$.browser.msie) {
    return $('.pagination a').live('click', function(e) {
      var $this;
      e.preventDefault();
      $this = $(this);
      if ($.scrollTo != null) {
        return $.scrollTo('#main', 500, function() {
          return $.get($this.attr('href'), function(data) {
            History.pushState({
              content: data,
              type: 'pagination'
            }, document.title, $this.attr('href'));
            return $('#main').html(data);
          });
        });
      } else {
        return $.get($this.attr('href'), function(data) {
          History.pushState({
            content: data,
            type: 'pagination'
          }, document.title, $this.attr('href'));
          return $('#main').html(data);
        });
      }
    });
  }
});

$(function() {
  return $('button#follow').length && (function() {
    var $btn, url;
    $btn = $('#follow');
    url = $btn.data('url');
    return $btn.on('click', function(e) {
      return $.post(url, function(data) {
        if (data.status === 'ok') {
          $btn.toggleClass('primary-btn');
          return $btn.text($btn.text() === '取消关注' ? '关注' : '取消关注');
        }
      });
    });
  })();
});

$(function() {
  if (typeof meta_photo !== "undefined" && meta_photo !== null) {
    return $.fancybox.open(get_open_options({
      href: meta_photo.url + "?single=yes",
      photo_width: meta_photo.width,
      photo_height: meta_photo.height
    }));
  }
});
