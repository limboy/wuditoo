from handlers import *

handlers = [
    (r"/", HomeHandler),
    (r"/register", RegisterHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/about", AboutHandler),

    (r"/photo/upload", PhotoUploadHandler),
    (r"/photo", PhotoHandler),
    (r"/photo/([0-9]+)/delete", PhotoDeleteHandler),
    (r"/photo/([0-9]+)/tagadd", PhotoTagAddHandler),
    (r"/photo/([0-9]+)/tagremove/([0-9]+)", PhotoTagRemoveHandler),
    (r"/photo/([0-9]+)/update", PhotoUpdateHandler),
    (r"/photo/([0-9]+)/via/user", PhotoUserHandler),
    (r"/photo/([0-9]+)/via/hot", PhotoHotHandler),
    (r"/photo/([0-9]+)/via/mine", PhotoMineHandler),
    (r"/photo/([0-9]+)/via/tag/([^/*]+)", PhotoTagHandler),
    (r"/photo/([0-9]+)", PhotoHandler),
    (r"/photo/([0-9]+)/like", PhotoLikeHandler),
    (r"/photos/hot", HotPhotosHandler),
    (r"/photos/latest", LatestPhotosHandler),
    (r"/tag/([^/*]+)", PhotosTagHandler),

    (r"/user/([a-zA-Z\-\_0-9]+)", UserHandler),
    (r"/user/([a-zA-Z\-\_0-9]+)/photos", UserPhotosHandler),
    (r"/user/([a-zA-Z\-\_0-9]+)/follow", UserFollowHandler),
    (r"/user/([a-zA-Z\-\_0-9]+)/following", UserFollowingHandler),
    (r"/user/([a-zA-Z\-\_0-9]+)/follower", UserFollowerHandler),

    (r"/mine/photos", MinePhotosHandler),
    (r"/mine/likes_photos", MineLikesPhotosHandler),
    (r"/mine/invite", MineInviteHandler),
    (r"/mine/following", MineFollowingHandler),
    (r"/mine/follower", MineFollowerHandler),

    (r"/settings", SettingsHandler),
    (r"/settings/profile", SettingsProfileHandler),
    (r"/settings/link", SettingsLinkHandler),
    (r"/settings/avatar", SettingsAvatarHandler),
    (r"/settings/password", SettingsPasswordHandler),

    (r"/comment/add", CommentAddHandler),
    (r"/comment/([0-9]+)/delete", CommentDeleteHandler),

    (r"/blog", BlogHandler),
    (r"/blog/([0-9]+)", BlogHandler),
    (r"/blog/([0-9]+)/comment", BlogCommentAddHandler),

]
