from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app_1 import views, dashboard
from app_1 import api, emails

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('contact-us/', views.contact, name = 'contact'),
    path('our-services/', views.services, name = 'services'),
    path('our-portfolio/', views.portfolio, name = 'portfolio'),
    path('our-blog-1/', views.blog_1, name = 'blog_1'),
    path('our-blog-2/', views.blog_2, name = 'blog_2'),
    path('your-cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('coming-soon/', views.coming_soon, name = 'coming_soon'),
    path('frequently-asked-questions/', views.faq, name = 'faq'),
    path('messages/', views.messages, name = 'messages'),
    path('our-portfolio-details/', views.portfolio_details, name = 'portfolio_details'),
    path('privacy-policy/', views.privacy_policy, name = 'privacy_policy'),
    path('service-details/', views.service_details, name = 'service_details'),
    path('our-services-1/', views.services_1, name = 'services_1'),
    path('our-services-2/', views.services_2, name = 'services_2'),
    path('our-shop-details/', views.shop_details, name = 'shop_details'),
    path('our-shop/', views.shop, name = 'shop'),
    path('sign-in/', views.sign_in, name = 'sign_in'),
    path('sign-up/', views.sign_up, name = 'sign_up'),
    path('single-team/', views.single_team, name = 'single_team'),
    path('our-team/', views.team, name = 'team'),
    path('our-terms-and-conditions/', views.terms_conditions, name = 'terms_conditions'),
    path('testimonials/', views.testimonials, name = 'testimonials'),
    path('not-found-404-page/', views.not_found_404_page, name = 'not_found_404_page'),
    #DASHBBOARD LINKS
    path('dashboard/', dashboard.projects_overview, name = 'projects_overview'),
    path('dashboard/sales-index/', dashboard.sales_index, name = 'sales_index'),

    path('dashboard/departments/', dashboard.departments, name = 'departments'),
    path('dashboard/departments/create-department/', dashboard.departments_create_department, name = 'departments-create-department'),
    path('dashboard/departments/department/<int:pk>/', dashboard.departments_department, name = 'departments-department'),

    path('dashboard/roles/', dashboard.roles, name = 'roles'),
    path('dashboard/roles/create-role/', dashboard.roles_create_role, name = 'roles-create-role'),
    path('dashboard/roles/role/<int:pk>/', dashboard.roles_role, name = 'roles-role'),

    path('dashboard/employment-types/', dashboard.employment_types, name = 'employment-types'),
    path('dashboard/employment-types/<int:pk>/', dashboard.employment_type, name = 'employment-type'),
    path('dashboard/employment-types/create/', dashboard.employment_types_create, name = 'employment-types-create'),


    path('dashboard/ecommerce/products/', dashboard.ecommerce_products, name = 'ecommerce_products'),
    path('dashboard/ecommerce/customers/', dashboard.ecommerce_customers, name = 'ecommerce_customers'),
    path('dashboard/ecommerce/customer-details/', dashboard.ecommerce_customer_details, name = 'ecommerce_customer_details'),
    path('dashboard/ecommerce/orders/', dashboard.ecommerce_orders, name = 'ecommerce_orders'),
    path('dashboard/ecommerce/order-details/', dashboard.ecommerce_order_details, name = 'ecommerce_order_details'),
    path('dashboard/ecommerce/refunds/', dashboard.ecommerce_refunds, name = 'ecommerce_refunds'),

    path('dashboard/create/clients/', dashboard.create_clients, name = 'create_clients'),
    path('dashboard/clients/', dashboard.clients, name = 'clients'),
    path('dashboard/client/<int:pk>/', dashboard.client, name = 'client'),

    path('dashboard/projects/overview/', dashboard.projects_overview, name = 'projects_overview'),
    path('dashboard/projects/', dashboard.projects, name = 'projects'),
    path('dashboard/project/<int:pk>/', dashboard.project, name = 'project'),
    path('dashboard/projects/board/', dashboard.projects_board, name = 'projects_board'),
    path('dashboard/projects/teams/', dashboard.projects_teams, name = 'projects_teams'),
    path('dashboard/projects/create-teams/', dashboard.projects_create_teams, name = 'projects_create_teams'),
    path('dashboard/create-projects/', dashboard.create_projects, name = 'create-projects'),
    path('dashboard/projects/files/', dashboard.projects_files, name = 'projects_files'),
    path('dashboard/folders/', dashboard.folders, name = 'manage-folders'),
    path('dashboard/create/folders/', dashboard.create_folders, name = 'create-folders'),
    path('dashboard/folder/<str:slug>/', dashboard.folder, name = 'folder'),

    path('dashboard/analytics/reports/', dashboard.analytics_reports, name = 'analytics_reports'),
    path('dashboard/analytics/customers/', dashboard.analytics_customers, name = 'analytics_customers'),

    path('dashboard/apps/chat/', dashboard.apps_chat, name = 'apps_chat'),
    path('dashboard/apps/contact-list/', dashboard.apps_contact_list, name = 'apps_contact_list'),
    path('dashboard/apps/calender/', dashboard.apps_calender, name = 'apps_calender'),
    path('dashboard/apps/invoice/', dashboard.apps_invoice, name = 'apps_invoice'),
    
    path('dashboard/employees/add/', dashboard.add_employees, name = 'add_employees'),
    path('dashboard/employees/list/', dashboard.list_employees, name = 'list_employees'),
    path('dashboard/employees/manage/', dashboard.manage_employees, name = 'manage_employees'),
    path('dashboard/employees/teams/', dashboard.teams_employees, name = 'teams_employees'),
    path('dashboard/employee/<int:pk>/', dashboard.employee, name = 'employee'),



    # UI
    path('dashboard/ui/alerts/', dashboard.ui_alerts, name='ui-alerts'),
    path('dashboard/ui/avatar/', dashboard.ui_avatar, name='ui-avatar'),
    path('dashboard/ui/buttons/', dashboard.ui_buttons, name='ui-buttons'),
    path('dashboard/ui/badges/', dashboard.ui_badges, name='ui-badges'),
    path('dashboard/ui/cards/', dashboard.ui_cards, name='ui-cards'),
    path('dashboard/ui/carousels/', dashboard.ui_carousels, name='ui-carousels'),
    path('dashboard/ui/dropdowns/', dashboard.ui_dropdowns, name='ui-dropdowns'),
    path('dashboard/ui/grids/', dashboard.ui_grids, name='ui-grids'),
    path('dashboard/ui/images/', dashboard.ui_images, name='ui-images'),
    path('dashboard/ui/list/', dashboard.ui_list, name='ui-list'),
    path('dashboard/ui/modals/', dashboard.ui_modals, name='ui-modals'),
    path('dashboard/ui/navs/', dashboard.ui_navs, name='ui-navs'),
    path('dashboard/ui/navbar/', dashboard.ui_navbar, name='ui-navbar'),
    path('dashboard/ui/offcanvas/', dashboard.ui_offcanvas, name='ui-offcanvas'),
    path('dashboard/ui/paginations/', dashboard.ui_paginations, name='ui-paginations'),
    path('dashboard/ui/popover-tooltips/', dashboard.ui_popover_tooltips, name='ui-popover-tooltips'),
    path('dashboard/ui/progress/', dashboard.ui_progress, name='ui-progress'),
    path('dashboard/ui/spinners/', dashboard.ui_spinners, name='ui-spinners'),
    path('dashboard/ui/tabs-accordions/', dashboard.ui_tabs_accordions, name='ui-tabs-accordions'),
    path('dashboard/ui/typography/', dashboard.ui_typography, name='ui-typography'),
    path('dashboard/ui/videos/', dashboard.ui_videos, name='ui-videos'),

    # Advanced
    path('dashboard/advanced/animation/', dashboard.advanced_animation, name='advanced_animation'),
    path('dashboard/advanced/clip-board/', dashboard.advanced_clip_board, name='advanced_clip_board'),
    path('dashboard/advanced/dragula/', dashboard.advanced_dragula, name='advanced_dragula'),
    path('dashboard/advanced/file-manager/', dashboard.advanced_file_manager, name='advanced_file_manager'),
    path('dashboard/advanced/highlight/', dashboard.advanced_highlight, name='advanced_highlight'),
    path('dashboard/advanced/range-slider/', dashboard.advanced_range_slider, name='advanced_range_slider'),
    path('dashboard/advanced/ratings/', dashboard.advanced_ratings, name='advanced_ratings'),
    path('dashboard/advanced/ribbons/', dashboard.advanced_ribbons, name='advanced_ribbons'),
    path('dashboard/advanced/sweet-alerts/', dashboard.advanced_sweet_alerts, name='advanced_sweet_alerts'),
    path('dashboard/advanced/toasts/', dashboard.advanced_toasts, name='advanced_toasts'),

    # Forms
    path('dashboard/forms/basic-elements/', dashboard.forms_basic_elements, name='forms-basic-elements'),
    path('dashboard/forms/advance-elements/', dashboard.forms_advance_elements, name='forms-advance-elements'),
    path('dashboard/forms/validation/', dashboard.forms_validation, name='forms-validation'),
    path('dashboard/forms/wizard/', dashboard.forms_wizard, name='forms-wizard'),
    path('dashboard/forms/editors/', dashboard.forms_editors, name='forms-editors'),
    path('dashboard/forms/file-upload/', dashboard.forms_file_upload, name='forms-file-upload'),
    path('dashboard/forms/image-crop/', dashboard.forms_image_crop, name='forms-image-crop'),

    # Charts
    path('dashboard/charts/apex/', dashboard.charts_apex, name='charts-apex'),
    path('dashboard/charts/justgage/', dashboard.charts_justgage, name='charts-justgage'),
    path('dashboard/charts/chatjs/', dashboard.charts_chatjs, name='charts-chartsjs'),
    path('dashboard/charts/toast/', dashboard.charts_toast, name='charts-toast'),

    # Tables
    path('dashboard/tables/basic/', dashboard.tables_basic, name='tables-basic'),
    path('dashboard/tables/datatables/', dashboard.tables_datatables, name='tables-datatables'),
    path('dashboard/tables/editable/', dashboard.tables_editable, name='tables-editable'),

    # Icons
    path('dashboard/icons/font-awesome/', dashboard.icons_font_awesome, name='icons-font-awesome'),
    path('dashboard/icons/line-awesome/', dashboard.icons_line_awesome, name='icons-line-awesome'),
    path('dashboard/icons/icofont/', dashboard.icons_icofont, name='icons-icofont'),
    path('dashboard/icons/iconoir/', dashboard.icons_iconoir, name='icons-iconoir'),

    # Maps
    path('dashboard/maps/google-maps/', dashboard.maps_google_maps, name='maps-google-maps'),
    path('dashboard/maps/leaflet-maps/', dashboard.maps_leaflet_maps, name='maps-leaflet-maps'),
    path('dashboard/maps/vector-maps/', dashboard.maps_vector_maps, name='maps-vector-maps'),

    # Email templates
    path('dashboard/email-templates/basic-action-email/', dashboard.email_templates_basic_action_email, name='email-templates-basic-action-email'),
    path('dashboard/email-templates/alert-email/', dashboard.email_templates_alert_email, name='email-templates-alert-email'),
    path('dashboard/email-templates/billing-email/', dashboard.email_templates_billing_email, name='email-templates-billing-email'),

    # Pages
    path('dashboard/pages/profile/<str:emp_id>/', dashboard.pages_profile, name='pages-profile'),
    path('dashboard/pages/notifications/', dashboard.pages_notifications, name='pages-notifications'),
    path('dashboard/pages/timeline/', dashboard.pages_timeline, name='pages-timeline'),
    path('dashboard/pages/treeview/', dashboard.pages_treeview, name='pages-treeview'),
    path('dashboard/pages/starter/', dashboard.pages_starter_page, name='pages-starter'),
    path('dashboard/pages/pricing/', dashboard.pages_pricing, name='pages-pricing'),
    path('dashboard/pages/blogs/', dashboard.pages_blogs, name='pages-blogs'),
    path('dashboard/pages/faqs/', dashboard.pages_faqs, name='pages-faq'),
    path('dashboard/pages/gallery/', dashboard.pages_gallery, name='pages-gallery'),

    # Authentication
    path('dashboard/auth/login/', dashboard.authentication_login, name='auth-login'),
    path('dashboard/auth/register/', dashboard.authentication_register, name='auth-register'),
    path('dashboard/auth/recover-pw/', dashboard.authentication_recover_pw, name='auth-recover-pw'),
    path('dashboard/auth/lock-screen/', dashboard.authentication_lock_screen, name='auth-lock-screen'),
    path('dashboard/auth/maintenance/', dashboard.authentication_maintenance, name='auth-maintenance'),
    path('dashboard/auth/404/', dashboard.authentication_404, name='auth-404'),
    path('dashboard/auth/403/', dashboard.authentication_403, name='auth-403'),
    path('dashboard/auth/500/', dashboard.authentication_500, name='auth-500'),
    
    

    #Staff Dashboard
    path('dashboard/staff/login/', dashboard.authentication_staff_login, name='auth-staff-login'),
    path('dashboard/staff/change-password/', dashboard.staff_change_password, name='change-password'),
    path('dashboard/staff/staff-dashboard/', dashboard.staff_dashboard, name='staff-dashboard'),
    path('dashboard/staff/staff-tasks/', dashboard.staff_tasks, name='staff-tasks'),
    path('dashboard/staff/staff-projects/', dashboard.staff_projects, name='staff-projects'),
    path('dashboard/staff/staff-profile/', dashboard.staff_profile, name='staff-profile'),
    path('dashboard/staff/staff-notifications/', dashboard.staff_notifications, name='staff-notifications'),
    path('dashboard/staff/staff-project/<int:pk>/', dashboard.staff_project, name='staff-project'),
    
    path('dashboard/create-company/', dashboard.create_company, name='create-company'),
    
    path('set-password/<str:link>/<str:token>/', dashboard.set_password, name = 'set-password'),
    path('create-main-admin/<str:link>/<str:token>', dashboard.create_main_admin, name='create-main-admin'),
    
    path('emails/check-email', emails.check_email, name='check-email'),



    #API LINKS
    path('api/', include('app_1.api.urls')),
    path('chat-api/', include('chat.api.urls')),
    #CHAT LINKS
    path('chat/', include('chat.urls')),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')

handler404 = "app_1.dashboard.custom_404"
handler500 = "app_1.dashboard.custom_500"