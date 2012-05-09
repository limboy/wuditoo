window.origin_title = document.title

# {{{ plugins
$.cookie = (name, value, options) ->
    if typeof value != 'undefined'
        options = options || {}
        if value == null
            value = "" 
            options.expires = -1
        expires = ""
        if options.expires and (typeof options.expires == 'number' or options.expires.toUTCString)
            if typeof options.expires == "number"
                date = new Date
                date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000))
            else
                date = options.expires
            # use expires attribute, max-age is not supported by IE
            expires = "; expires=#{date.toUTCString()}" 
        path = if options.path then "; path=#{(options.path)}" else ""
        domain = if options.domain then "; domain=#{options.domain}" else ""
        secure = if options.secure then "; secure=#{options.secure}" else ""
        document.cookie = [name, "=", encodeURIComponent(value), expires, path, domain, secure].join("")
    else # only name given, get cookie
        cookieValue = null
        if document.cookie and document.cookie != ""
            cookies = document.cookie.split(";")
            for cookie in cookies
                cookie = jQuery.trim(cookie)
                if cookie.substring(0, (name.length + 1)) == ("#{name}=")
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                    break
        # return the value of cookieValue
        cookieValue
# }}}

# {{{ utils
photoUploadDone = (result) ->
    if result.status == 'ok'
        if result.content.location
            window.location = result.content.location
    else
        $btn = $('#photo-upload').find('.disabled')
        $btn.removeClass('disabled').val($btn.data('origin_text'))
        $('.error').hide()
        for key, val of result.content
            $("##{key}-error").html(val).show()


avatarUploadDone = (result) ->
    $form = $('#avatar-upload')
    $form.find('.success').hide()
    $submit_btn  = $form.find('input[type="submit"]')
    $submit_btn.removeClass('disabled')
        .val($submit_btn.data('origin_text'))
    if result.status == 'ok'
        $form.find('.avatar img').attr('src', result.content.avatar_url)
        $form.find('.success').show()
    else
        $('.error').hide()
        for key, val of result.content
            $("##{key}-error").html(val).show()


resizePhoto = (container_width, container_height, photo_width, photo_height) ->
    width_ratio = photo_width / container_width
    height_ratio = photo_height / container_height

    resized_photo_width = photo_width
    resized_photo_height = photo_height

    if width_ratio > height_ratio and photo_width > container_width
        resized_photo_width = container_width
        resized_photo_height = photo_height / width_ratio
    else if height_ratio > width_ratio and photo_height > container_height
        resized_photo_height = container_height
        resized_photo_width = photo_width / height_ratio
    return [parseInt(resized_photo_width), parseInt(resized_photo_height)]


adjustFancybox = (photo_width = 0, photo_height = 0) ->
    if not photo_width
        current = $.fancybox.current
        $item = $(current.element)
        photo_width = $item.data('photo-width')
        photo_height = $item.data('photo-height')
        if not photo_width and meta_photo?
            photo_width = meta_photo.width
            photo_height = meta_photo.height

    if photo_width
        photo_extra_width = if $('#photo-extra').width() == 0 then 0 else $('#photo-extra').innerWidth()
        container_width = $('.fancybox-outer').width() - photo_extra_width
        container_height = $('.fancybox-outer').height()
        [resized_photo_width, resized_photo_height] = resizePhoto(
            container_width, container_height, photo_width, photo_height
        )
        $('#photo img').css({
            width: resized_photo_width+'px', 
            height: resized_photo_height+'px', 
            'margin-left': '-'+parseInt(resized_photo_width/2)+'px',
            'margin-top': '-'+parseInt(resized_photo_height/2)+'px',
            display: 'block'})

        $('#photo').css({width: container_width, height: container_height})
        $('#photo .left, #photo .right').css({
            width: parseInt(container_width/2),
            height: container_height
        })
        $('#photo-extra').css('height', ($('.fancybox-inner').height()-30)+'px')


get_open_options = (opts = {}) ->
    defaults = {
        type : 'ajax',
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
        afterShow: ->
            if $.cookie('photofullsize')
                $('#photo-extra').hide().width(0)
                $('#photo .toggle-fullsize').addClass('icon-resize-small')
            $item = $($.fancybox.current.element)
            if opts.photo_width?
                adjustFancybox(opts.photo_width, opts.photo_height)
            else
                adjustFancybox()
            # push to history
            if History.enabled and not $.browser.msie
                window.opening_fancybox = true
                History.pushState({content: $('.fancybox-inner').html(), type: 'fancybox', index: $.fancybox.current.index}, $item.data('title'), $item.data('url'))
                window.opening_fancybox = false
        beforeShow: ->
            $('#photo img').hide()
        onUpdate: ->
            if opts.photo_width?
                adjustFancybox(opts.photo_width, opts.photo_height)
            else
                adjustFancybox()
        afterClose: (current) ->
            if History.enabled and not $.browser.msie
                History.pushState({}, window.origin_title, window.origin_location)
    }
    $.extend(defaults, opts)
    return defaults


$.fn.photoToggleSidebarIcon = ->
    this.on('click', (e) ->
        $(this).next().toggle()
        $(this).find('i').toggleClass('icon-slidedown')
    )

$.fn.photoLike = ->
    this.on('click', (e) ->
        e.preventDefault()
        $this = $(this)
        $icon = $this.find('i')
        $.post($this.data('url'), (data) ->
            $like_count = $this.next().find('.like-count')
            if data.status == 'ok'
                if $icon.hasClass('icon-liked-btn')
                    $icon.removeClass('icon-liked-btn').addClass('icon-like-btn')
                    current_count = parseInt($like_count.text())
                    $like_count.text(current_count-1)
                else
                    $icon.removeClass('icon-like-btn').addClass('icon-liked-btn')
                    current_count = parseInt($like_count.text())
                    $like_count.text(current_count+1)
        )
    )

$.fn.photoPrev = ->
    this.on('mouseover', (e) ->
        $(this).next().fadeIn('fast')
        $(this).next().next().next().fadeOut('fast')
        ).on('mouseout', (e) ->
        $(this).next().fadeOut('fast')
        ).on('click', (e) ->
            $.fancybox.prev()
    )

$.fn.photoNext = ->
    this.on('mouseover', (e) ->
        $(this).next().fadeIn('fast')
        $(this).prev().fadeOut('fast')
        ).on('mouseout', (e) ->
        $(this).next().fadeOut('fast')
        ).on('click', (e) ->
            $.fancybox.next()
    )

$.fn.photoCommentAdd = ->
    this.on('submit', (e) ->
        e.preventDefault()
        $this = $(this)
        $.post(
            $this.attr('action')
            $this.serialize()
            (result) ->
                if result.status == 'ok'
                    $('#comment-create input[type="text"]').val('')
                    $('#comment-create').before(result.content.content)
        )
    )

$.fn.photoCommentHover = ->
    this.on('mouseover', '.comment', (e) ->
        $(this).find('a.close').show()
        ).on('mouseout', '.comment', (e) ->
        $(this).find('a.close').hide()
        ).on('click', '.comment a.close', (e) ->
            e.preventDefault()
            $this = $(this)
            $.post($this.attr('href'), (result) ->
                if result.status == 'ok'
                    $comment = $this.parent().parent().parent()
                    $comment.next().fadeOut()
                    $comment.fadeOut()
            )
        )

$.fn.photoContentEdit = ->
    this.on('click', (e) ->
        $parent = $(this).parent().parent()
        $parent.hide()
        $parent.next().show()
    )

$.fn.photoContentCancelEdit = ->
    this.on('click', (e) ->
        $parent = $(this).parent().parent().parent()
        $parent.hide()
        $parent.prev().show()
    )

$.fn.photoContentSubmit = ->
    this.on('submit', (e) ->
        e.preventDefault()
        $this = $(this)
        $submit_btn  = $this.find('input[type="submit"]')
        $.post(
            $this.attr('action'),
            $this.serialize(),
            (result) ->
                $submit_btn.removeClass('disabled')
                    .val($submit_btn.data('origin_text'))
                if result.status == 'ok'
                    $('#photo-content h3 span').text(
                        $this.find('input[name="title"]').val())
                    $('#photo-content .content').html(
                        $this.find('textarea[name="content"]').val())
                    $this.parent().hide()
                    $this.parent().prev().show()
        )
    )

$.fn.photoTagHover = ->
    this.on('mouseover', 'li', (e) ->
        $(this).find('.close').css('visibility', 'visible')
        ).on('mouseout', 'li', (e) ->
        $(this).find('.close').css('visibility', 'hidden')
    )

$.fn.photoTagAdd = ->
    this.on('click', (e) ->
        e.preventDefault()
        e.stopPropagation()
        $(this).parent().hide()
        $('#tagadd').show()
    )

$.fn.photoTagAddCancel = ->
    this.on('click', (e) ->
        e.preventDefault()
        $(this).parent().parent().hide()
        $('#addtag').show()
    )

$.fn.photoTagAddSubmit = ->
    this.on('submit', (e) ->
        e.preventDefault()
        $this = $(this)
        $submit_btn = $this.find('input[type="submit"]')
        $.post(
            $this.attr('action')
            $this.serialize()
            (result) ->
                $submit_btn.removeClass('disabled')
                    .val($submit_btn.data('origin_text'))
                if result.status == 'ok'
                    for tag in result.content.tags
                        $('#tags').append("
                        <li><i class='icon-tag'></i> <a href='/tag/#{tag}'>#{tag}</a>
                        <span class='close invisible'>×</span></li>") 
        )
    )

$.fn.photoTagClose = ->
    this.on('click', (e) ->
        e.preventDefault()
        $this = $(this)
        $.post(
            $this.data('url'),
            (result) ->
                if result.status == 'ok'
                    $this.parent().fadeOut()
            'json'
        )
    )

$.fn.photoDelete = ->
    this.on('click', (e) ->
        $(this).hide().next().show()
    )

$.fn.photoDeleteCancel = ->
    this.on('click', (e) ->
        e.preventDefault()
        $(this).parent().hide().prev().show()
    )

$.fn.photoToggleFullsize = ->
    this.on('click', (e) ->
        $this = $(this)
        $this.toggleClass('icon-resize-small')
        if $this.hasClass('icon-resize-small')
            $('#photo-extra').width(0)
            $('#photo-extra').hide()
            $.cookie('photofullsize', 1)
        else
            $('#photo-extra').width(285)
            $('#photo-extra').show()
            $.cookie('photofullsize', '')
        adjustFancybox()
    )

$.fn.photoDeleteSubmit = ->
    this.on('click', (e) ->
        e.preventDefault()
        $this = $(this)
        $.post(
            $this.data('url')
            (result) ->
                if result.status == 'ok'
                    window.location = result.content.location
            'json'
        )
    )

$.fn.ajaxSubmit = ->
    this.on('submit', (e) ->
        $this = $(this)
        $submit_btn = $this.find('input[type="submit"]')
        $this.find('.error').hide()
        $this.find('.success').hide()
        e.preventDefault()
        $.post(
            $this.attr('action')
            $this.serialize()
            (result) ->
                $submit_btn.removeClass('disabled')
                    .val($submit_btn.data('origin_text'))
                if result.status == 'ok'
                    if result.content.location?
                        window.location = result.content.location
                    else
                        $this.find('.success').show()
                else
                    for key, val of result.content
                        $("##{key}-error").html(val).show()
            'json')
    )

$.fn.userFollow = ->
    this.on('click', (e) ->
        $btn = $(this)
        url = $btn.data('url')
        $.post(url, (data) ->
            if data.status == 'ok'
                $btn.toggleClass('primary-btn')
                $btn.text(
                    if $btn.text() == '取消关注' then '关注' else '取消关注'
                )
        )
    )

$.fn.photosFancy = ->
    this.on('click', (e) ->
        e.preventDefault()
        window.origin_location = location.href
        $.fancybox.open($('#photos a.fancybox'), get_open_options(
            {index: $(this).data('index')}
        ))
    )

# }}}

# {{{ base settings
$ ->
    $('#sidebar .item').length && do () ->
        # used for history change, highlight dest trigger
        $('#sidebar .item').each( (index) ->
            $(this).attr('vid', "item-#{index}")
        )

        $('#sidebar').on('click', '.item', (e) ->
            e.preventDefault()
            $this = $(this)

            if History.enabled and ! $.browser.msie
                if $this.hasClass('disabled')
                    return
                $('.item').removeClass('highlight')
                $this.addClass('highlight')
                url = $this.data('url')
                vid = $this.attr('vid')
                $.get(url, (data) ->
                    History.pushState({content: data, vid: vid, type: 'sidebar_item'}, $this.data('title'), url)
                    $('#main').html(data)
                )
            else
                window.location = $this.data('url')
        )

    $('input.btn').live('click', (e) ->
        $this = $(this)
        if $this.hasClass('disabled')
            return false
        $this.data('origin_text', $this.val())
        $this.addClass('disabled')
        $this.val('working...')
        return true
        )

    # 在监听前先放入当前的内容, 将来可以回退到最开始的状态
    if History.enabled and not $.browser.msie and $('#main').html()
        History.pushState({type: 'sidebar_item', content: $('#main').html(), vid: 'nonexists'}, document.title, location.pathname+location.search)

        History.Adapter.bind(window, 'statechange', ->
            state = History.getState()
            if not state.data
                return
            document.title = state.title
            if state.data.type != 'fancybox'
                $('#main').html(state.data.content)
                $.fancybox.close()
            if state.data.type == 'sidebar_item'
                $('.item').removeClass('highlight')
                $("[vid=#{state.data.vid}]").addClass('highlight')
            if state.data.type == 'fancybox'
                if not $('#main').html()
                    window.location.reload()
                if not window.opening_fancybox
                    if not $.fancybox.isOpen
                        $.fancybox.open($('#photos a.fancybox'), get_open_options())
                    $.fancybox.jumpto(state.data.index)
                    adjustFancybox()
            )

    if History.enabled and not $.browser.msie
        $('.pagination a').live('click', (e) ->
            e.preventDefault()
            $this = $(this)
            if $.scrollTo?
                $.scrollTo('#main', 500, ->
                    $.get($this.attr('href'), (data) ->
                        History.pushState({content: data, type: 'pagination'}, document.title, $this.attr('href'))
                        $('#main').html(data)
                    )
                )
            else
                $.get($this.attr('href'), (data) ->
                    History.pushState({content: data, type: 'pagination'}, document.title, $this.attr('href'))
                    $('#main').html(data)
                )
        )

# }}}

# {{{ business
$ ->
    $('button#follow').length && do() ->
        $btn = $('#follow')
        url = $btn.data('url')
        $btn.on('click', (e)->
            $.post(url, (data) ->
                if data.status == 'ok'
                    $btn.toggleClass('primary-btn')
                    $btn.text(
                        if $btn.text() == '取消关注' then '关注' else '取消关注'
                    )
            )
        )

# }}}

# {{{ metadata
$ ->
    if meta_photo?
        $.fancybox.open(get_open_options({
            href: meta_photo.url+"?single=yes",
            photo_width: meta_photo.width,
            photo_height: meta_photo.height
        }))
# }}}
