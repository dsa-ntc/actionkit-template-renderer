from django.db import models

###
# Order of models based on grouping in AK DB reference guide
###
"""
Missing from here but seen in documentation:
https://roboticdogs.actionkit.com/docs/manual/developer/wmd.html#core-eventvolunteeraction
https://roboticdogs.actionkit.com/docs/manual/developer/wmd.html#gm-subscriptioncounthistory
https://roboticdogs.actionkit.com/docs/manual/developer/wmd.html#cms-event-volunteer-form
https://roboticdogs.actionkit.com/docs/manual/developer/wmd.html#zip-proximity
https://roboticdogs.actionkit.com/docs/manual/developer/wmd.html#numeric-date
https://roboticdogs.actionkit.com/docs/manual/developer/wmd.html#numeric-9999
https://roboticdogs.actionkit.com/docs/manual/developer/wmd.html#numeric-digit
Guessing these may have been removed but not removed from documentation,
as there's also models here that aren't in documentation
"""


# Staff User Tables
class AuthUser(models.Model):
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=128)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "auth_user"


# Action Tables
class CoreAction(models.Model):
    """Every action submitted with associated user_id, page_id, and source."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)
    mailing = models.ForeignKey("CoreMailing", models.DO_NOTHING, blank=True, null=True)
    page = models.ForeignKey("CorePage", models.DO_NOTHING)
    link = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=255)
    opq_id = models.CharField(max_length=255)
    created_user = models.IntegerField()
    subscribed_user = models.IntegerField()
    referring_user = models.ForeignKey(
        "CoreUser",
        models.DO_NOTHING,
        related_name="referred_action",
        blank=True,
        null=True,
    )
    referring_mailing = models.ForeignKey(
        "CoreMailing",
        models.DO_NOTHING,
        related_name="referred_action",
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=255)
    taf_emails_sent = models.IntegerField(blank=True, null=True)
    is_forwarded = models.IntegerField()
    ip_address = models.CharField(max_length=15, blank=True, null=True)
    useragent = models.ForeignKey(
        "CoreUserAgent", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "core_action"


class CoreActionField(models.Model):
    """Custom action fields; answers to survey questions (from any page type)."""

    parent = models.ForeignKey(CoreAction, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = "core_actionfield"


class CoreActionNotification(models.Model):
    """Notification email to be sent to someone aside from the actiontaker after an action."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(max_length=255)
    to = models.TextField(blank=True, null=True)
    from_line = models.ForeignKey(
        "CoreFromLine", models.DO_NOTHING, blank=True, null=True
    )
    custom_from = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True, null=True)
    wrapper = models.ForeignKey(
        "CoreEmailWrapper", models.DO_NOTHING, blank=True, null=True
    )
    body = models.TextField(blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_actionnotification"


class CoreActionNotificationToStaff(models.Model):
    """Joins notification email from above with one or more staff user_ids to receive it."""

    actionnotification = models.ForeignKey(CoreActionNotification, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_actionnotification_to_staff"
        unique_together = (("actionnotification", "user"),)


class CoreCallAction(models.Model):
    """Records every call action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_callaction"


class CoreCallActionChecked(models.Model):
    """Identifies which of the targets displayed on a call page the user indicated they called."""

    callaction = models.ForeignKey(CoreCallAction, models.DO_NOTHING)
    target = models.ForeignKey("CoreTarget", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_callaction_checked"
        unique_together = (("callaction", "target"),)


class CoreCallActionLocalOfficeChecked(models.Model):
    """Identifies which office the user indicated they called (if local offices were shown on the call page)."""

    callaction = models.ForeignKey(CoreCallAction, models.DO_NOTHING)
    targetoffice = models.ForeignKey("CoreTargetOffice", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_callaction_local_office_checked"
        unique_together = (("callaction", "targetoffice"),)


class CoreCallActionTargeted(models.Model):
    """Identifies who showed as targets for a specific user on a specific call page."""

    callaction = models.ForeignKey(CoreCallAction, models.DO_NOTHING)
    target = models.ForeignKey("CoreTarget", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_callaction_targeted"
        unique_together = (("callaction", "target"),)


class CoreCampaignVolunteerAction(models.Model):
    """Records every volunteer moderator signup submitted and joins to core_action as well as the event campaign."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)
    campaign = models.ForeignKey("EventsCampaign", models.DO_NOTHING)
    volunteer = models.ForeignKey("EventsCampaignVolunteer", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_campaignvolunteeraction"


class CoreDonationAction(models.Model):
    """Records every donation action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_donationaction"


class CoreDonationUpdateAction(models.Model):
    """Records every donationupdate action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_donationupdateaction"


class CoreDonationCancellationAction(models.Model):
    """Records every donationcancellation action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_donationcancellationaction"


class CoreEventCreateAction(models.Model):
    """Joins each event creation action in core_action to the event. Also links to the events table."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)
    event = models.ForeignKey("Event", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_eventcreateaction"


class CoreEventModerateAction(models.Model):
    """Joins each event moderation action in core_action to the event."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)
    event = models.ForeignKey("Event", models.DO_NOTHING)
    approved_event = models.IntegerField()
    deleted_event = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_eventmoderateaction"


class CoreEventSignupAction(models.Model):
    """Joins attendee sign up in core_action to sign up record."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)
    signup = models.ForeignKey("EventSignup", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_eventsignupaction"


class CoreImportAction(models.Model):
    """Records every import action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_importaction"


class CoreLetterAction(models.Model):
    """Records every letter action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_letteraction"


class CoreLetterActionTargeted(models.Model):
    letteraction = models.ForeignKey(CoreLetterAction, models.DO_NOTHING)
    target = models.ForeignKey("CoreTarget", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_letteraction_targeted"
        unique_together = (("letteraction", "target"),)


class CoreLteAction(models.Model):
    """Joins each LTE action in core_action to the newspaper and includes the letter text. Also includes the users letter."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)
    subject = models.CharField(max_length=80)
    letter_text = models.TextField()
    target = models.ForeignKey(
        "CoreMediaTarget", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "core_lteaction"


class CorePetitionAction(models.Model):
    """Records every petition action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_petitionaction"


class CorePetitionActionTargeted(models.Model):
    petitionaction = models.ForeignKey(CorePetitionAction, models.DO_NOTHING)
    target = models.ForeignKey("CoreTarget", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_petitionaction_targeted"
        unique_together = (("petitionaction", "target"),)


class CoreRecurringDonationCancelAction(models.Model):
    """Records every recurringdonationcancel action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_recurringdonationcancelaction"


class CoreRecurringDonationUpdateAction(models.Model):
    """Records every recurringdonationupdate action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_recurringdonationupdateaction"


class CoreRedirectAction(models.Model):
    """Records every redirect action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_redirectaction"


class CoreSignupAction(models.Model):
    """Records every signup action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_signupaction"


class CoreSurveyAction(models.Model):
    """Records every survey action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_surveyaction"


class CoreUnsubscribeAction(models.Model):
    """Records every unsubscribe action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_unsubscribeaction"


class CoreUserUpdateAction(models.Model):
    """Records every userupdate action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_userupdateaction"


class CoreWhipcountAction(models.Model):
    """Records every whipcount action submitted and joins to core_action."""

    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_whipcountaction"


class CoreWhipcountActionCalled(models.Model):
    """Records who was called for each whipcount action and the response recorded by the user."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    target = models.ForeignKey("CoreTarget", models.DO_NOTHING)
    whipcountaction = models.ForeignKey(CoreWhipcountAction, models.DO_NOTHING)
    response = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_whipcountactioncalled"


class SpamCheckLog(models.Model):
    """A history of actions that looked like spambots, malicious users, or that matched blacklists or whitelists."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    check = models.CharField(max_length=255)
    why = models.TextField(blank=True, null=True)
    whitelisted = models.IntegerField()
    action = models.ForeignKey(CoreAction, models.DO_NOTHING)
    action_status = models.CharField(max_length=255)
    action_updated_at = models.DateTimeField()
    reversed = models.IntegerField()
    reversed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "spam_spamchecklog"


# Page Tables
class CoreLanguage(models.Model):
    """Name of language and error translations you've entered for any additional languages (aside from English)."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    translations = models.TextField()
    hidden = models.IntegerField()
    iso_code = models.CharField(max_length=10, blank=True, null=True)
    inherit_from_id = models.IntegerField(blank=True, null=True)
    ordering = models.IntegerField(blank=True, null=True)
    is_default = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_language"


class CoreMultilingualCampaign(models.Model):
    """Join translations of a page together for reporting and for your end users."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = "core_multilingualcampaign"


class CorePage(models.Model):
    """Unique id for each page and basic info including name, goal, page type."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    title = models.CharField(max_length=255)
    name = models.CharField(unique=True, max_length=255)
    notes = models.CharField(max_length=255, blank=True, null=True)
    hosted_with = models.ForeignKey("CoreHostingPlatform", models.DO_NOTHING)
    url = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    lang = models.ForeignKey(CoreLanguage, models.DO_NOTHING, blank=True, null=True)
    multilingual_campaign = models.ForeignKey(
        CoreMultilingualCampaign, models.DO_NOTHING, blank=True, null=True
    )
    goal = models.IntegerField(blank=True, null=True)
    goal_type = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    list = models.ForeignKey("CoreList", models.DO_NOTHING)
    hidden = models.IntegerField()
    allow_multiple_responses = models.IntegerField()
    recognize = models.CharField(max_length=255)
    never_spam_check = models.IntegerField()
    real_actions = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_page"


class CorePageGroups(models.Model):
    """Associates a page with one or more groups."""

    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    usergroup = models.ForeignKey("CoreUserGroup", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_page_groups"
        unique_together = (("page", "usergroup"),)


class CoreAllowedPageField(models.Model):
    """Custom field created by your group to display text or activate custom code on a particular page."""

    name = models.CharField(
        primary_key=True, max_length=255, db_collation="utf8mb3_general_ci"
    )
    hidden = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    always_show = models.IntegerField()
    display_name = models.CharField(unique=True, max_length=255)
    order_index = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    field_default = models.TextField()
    field_choices = models.TextField()
    field_regex = models.TextField()
    field_type = models.CharField(max_length=32, db_collation="utf8mb3_general_ci")
    field_length = models.IntegerField(blank=True, null=True)
    required = models.IntegerField()
    allow_multiple = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_allowedpagefield"


class CoreBuiltinTranslation(models.Model):
    """ActionKit provided language translations for error messages, form fields, etc."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(unique=True, max_length=255)
    iso_code = models.CharField(max_length=10)
    translations = models.TextField()

    class Meta:
        managed = False
        db_table = "core_builtintranslation"


class CoreCallPage(models.Model):
    """Page id for all pages of type call and page specific attributes (like whether only constituents can take this action)."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)
    constituents_only_url = models.CharField(max_length=200)
    allow_local_targetoffices = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_callpage"


class CoreCallPageTargetGroups(models.Model):
    """Joins call page to targets."""

    callpage = models.ForeignKey(CoreCallPage, models.DO_NOTHING)
    targetgroup = models.ForeignKey("CoreTargetGroup", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_callpage_target_groups"
        unique_together = (("callpage", "targetgroup"),)


class CoreCampaignVolunteerPage(models.Model):
    """Page ID for all volunteer event moderator signup pages and campaign the page is associated with."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)
    campaign = models.ForeignKey("EventsCampaign", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_campaignvolunteerpage"


class CoreDonationPage(models.Model):
    """Page id for all pages of type donation and page specific attributes."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_account = models.CharField(max_length=255)
    hpc_rule = models.ForeignKey(
        "CoreDonationHpcRule", models.DO_NOTHING, blank=True, null=True
    )
    allow_international = models.IntegerField()
    filtering_for_web = models.ForeignKey(
        "CoreDonationFraudFilter",
        models.DO_NOTHING,
        related_name="web_donation",
        blank=True,
        null=True,
    )
    filtering_for_mailings = models.ForeignKey(
        "CoreDonationFraudFilter",
        models.DO_NOTHING,
        related_name="mailing_donation",
        blank=True,
        null=True,
    )
    use_account_switcher = models.IntegerField(blank=True, null=True)
    paypal_account = models.CharField(max_length=255, blank=True, null=True)
    paypal_user_requirements = models.CharField(max_length=255)
    accept_ach = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_donationpage"


class CoreDonationCancellationPage(models.Model):
    """Page id for all pages of type Cancel Recurring Donation and page specific attributes."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_donationcancellationpage"


class CoreDonationUpdatePage(models.Model):
    """Page id for all pages of type Update Rcurring Donation and page specific attributes."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_donationupdatepage"


class CoreEventCreatePage(models.Model):
    """Joins event campaign to the event creation page."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)
    campaign = models.ForeignKey("EventsCampaign", models.DO_NOTHING)
    campaign_title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_eventcreatepage"


class CoreEventModeratePage(models.Model):
    """Joins event moderation page to the event campaign."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)
    campaign = models.ForeignKey("EventsCampaign", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_eventmoderatepage"


class CoreEventSignupPage(models.Model):
    """Joins event signup to the event campaign."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)
    campaign = models.ForeignKey("EventsCampaign", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_eventsignuppage"


class CoreFormField(models.Model):
    """Default fields available for inclusion in forms (name, state, etc.)"""

    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = "core_formfield"


class CoreImmediateDeliveryLog(models.Model):
    """Logs every immediate delivery sent. Joins to core_action."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(max_length=255, blank=True, null=True)
    action = models.ForeignKey(CoreAction, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_immediatedeliverylog"


class CoreImmediateDeliveryWarning(models.Model):
    """Used to generate message to switch to bulk delivery to admin if immediate delivery limit is exceeded."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_immediatedeliverywarning"


class CoreImportPage(models.Model):
    """Page id for all pages of type import and page specific attributes."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)
    subscribe = models.IntegerField(blank=True, null=True)
    default_source = models.CharField(max_length=255, blank=True, null=True)
    unsubscribe_all = models.IntegerField(blank=True, null=True)
    unsubscribe = models.IntegerField(blank=True, null=True)
    privacy_notes = models.ForeignKey(
        "CorePrivacyNotes", models.DO_NOTHING, blank=True, null=True
    )
    custom_privacy_notes = models.TextField()
    subscribe_if_new = models.IntegerField()
    texting_subscribe = models.IntegerField()
    texting_list_id = models.IntegerField(blank=True, null=True)
    texting_match = models.IntegerField()
    texting_match_phone_max_age = models.IntegerField()
    texting_match_name = models.CharField(max_length=20)
    texting_match_location = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_importpage"


class CoreLetterPage(models.Model):
    """Page id for all pages of type letter and page specific attributes."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)
    send_immediate_fax = models.IntegerField(blank=True, null=True)
    send_immediate_email = models.IntegerField(blank=True, null=True)
    send_immediate_email_override_limit = models.IntegerField()
    email_mode = models.IntegerField(blank=True, null=True)
    remind_me_set_up_batch_delivery = models.IntegerField()
    immediate_email_subject = models.TextField(blank=True, null=True)
    delivery_template = models.TextField(blank=True, null=True)
    batch_delivery_from = models.ForeignKey(
        "CoreFromLine", models.DO_NOTHING, blank=True, null=True
    )
    batch_delivery_subject = models.CharField(max_length=255, blank=True, null=True)
    batch_delivery_template = models.TextField(blank=True, null=True)
    batch_petitiondeliveryjob_id = models.IntegerField(blank=True, null=True)
    send_immediate_email_delivery_blocked_at = models.DateTimeField(
        blank=True, null=True
    )
    batch_delivery_threshold = models.IntegerField(blank=True, null=True)
    batch_delivery_minimum = models.IntegerField()
    send_via_cwc = models.IntegerField(blank=True, null=True)
    cwc_topic = models.CharField(max_length=255, blank=True, null=True)
    cwc_statement = models.TextField(blank=True, null=True)
    cwc_subject = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_letterpage"


class CoreLetterPageTargetGroups(models.Model):
    """Joins letter page to targets."""

    letterpage = models.ForeignKey(CoreLetterPage, models.DO_NOTHING)
    targetgroup = models.ForeignKey("CoreTargetGroup", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_letterpage_target_groups"
        unique_together = (("letterpage", "targetgroup"),)


class CoreSignatureTemplate(models.Model):
    """Template for user signature for LTEs."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(unique=True, max_length=255)
    is_default = models.IntegerField()
    template = models.TextField()

    class Meta:
        managed = False
        db_table = "core_signaturetemplate"


class CoreLtePage(models.Model):
    """Page id for all pages of type letter to the editor and page specific attributes such as selections made during set up for types of papers and whether to show phone number."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)
    national_newspapers = models.IntegerField()
    regional_newspapers = models.IntegerField()
    local_newspapers = models.IntegerField()
    show_phones = models.IntegerField()
    signature_template = models.ForeignKey(CoreSignatureTemplate, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_ltepage"


class CorePageRequiredFields(models.Model):
    """Fields required for the user to submit the given page, selected from the formfields above."""

    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    formfield = models.ForeignKey(CoreFormField, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_page_required_fields"
        unique_together = (("page", "formfield"),)


class CorePageTags(models.Model):
    """Associates a page with a tag or tags."""

    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    tag = models.ForeignKey("CoreTag", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_page_tags"
        unique_together = (("page", "tag"),)


class CorePageVisibleFields(models.Model):
    """Shows the fields you selected as required on the Action Basics screen when creating the page."""

    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    formfield = models.ForeignKey(CoreFormField, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_page_visible_fields"
        unique_together = (("page", "formfield"),)


class CorePageField(models.Model):
    """Page and page field value."""

    parent = models.ForeignKey(CorePage, models.DO_NOTHING)
    name = models.ForeignKey(CoreAllowedPageField, models.DO_NOTHING, db_column="name")
    value = models.TextField()

    class Meta:
        managed = False
        db_table = "core_pagefield"


class CorePageFollowup(models.Model):
    """Landing page, confirmation email, TAF and sharing for all pages."""

    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    send_email = models.IntegerField()
    url = models.CharField(max_length=255)
    email_wrapper = models.ForeignKey(
        "CoreEmailWrapper", models.DO_NOTHING, blank=True, null=True
    )
    email_from_line = models.ForeignKey(
        "CoreFromLine", models.DO_NOTHING, blank=True, null=True
    )
    email_custom_from = models.CharField(max_length=255)
    email_subject = models.CharField(max_length=255, blank=True, null=True)
    email_body = models.TextField(blank=True, null=True)
    send_taf = models.IntegerField()
    taf_subject = models.CharField(max_length=255, blank=True, null=True)
    taf_body = models.TextField(blank=True, null=True)
    share_title = models.CharField(max_length=255, blank=True, null=True)
    share_description = models.CharField(max_length=1024, blank=True, null=True)
    share_image = models.CharField(max_length=1024, blank=True, null=True)
    twitter_message = models.CharField(max_length=280, blank=True, null=True)
    send_notifications = models.IntegerField()
    send_pushes = models.IntegerField()
    send_texts = models.IntegerField()
    confirmation_text = models.ForeignKey(
        "TextingAfterActionMessage", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "core_pagefollowup"


class CorePageFollowupNotifications(models.Model):
    """Joins the page followup to the notification."""

    pagefollowup = models.ForeignKey(CorePageFollowup, models.DO_NOTHING)
    actionnotification = models.ForeignKey(CoreActionNotification, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_pagefollowup_notifications"
        unique_together = (("pagefollowup", "actionnotification"),)


class CorePrintTemplate(models.Model):
    """Defines the appearance of the cover letter and signature pages for delivery jobs."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    header_html = models.TextField()
    template = models.TextField()
    footer_html = models.TextField()
    font_family = models.CharField(max_length=255)
    font_size = models.FloatField()
    logo_url = models.CharField(max_length=200)
    page_size = models.CharField(max_length=255)
    margin_units = models.CharField(max_length=255)
    margin_top = models.FloatField()
    margin_bottom = models.FloatField()
    margin_left = models.FloatField()
    margin_right = models.FloatField()
    readonly = models.IntegerField()
    hidden = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_printtemplate"


class CorePetitionDeliveryJob(models.Model):
    """Defines the content, delivery options, and appearance for each delivery job."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    single_file = models.IntegerField()
    cover_html = models.TextField()
    print_template = models.ForeignKey(CorePrintTemplate, models.DO_NOTHING)
    header_content = models.TextField()
    footer_content = models.TextField()
    allow_pdf_download = models.IntegerField(blank=True, null=True)
    allow_csv_download = models.IntegerField(blank=True, null=True)
    include_prefix_in_csv = models.IntegerField()
    include_first_name_in_csv = models.IntegerField()
    include_middle_name_in_csv = models.IntegerField()
    include_last_name_in_csv = models.IntegerField()
    include_suffix_in_csv = models.IntegerField()
    template_set = models.ForeignKey(
        "CmsTemplateSet", models.DO_NOTHING, blank=True, null=True
    )
    limit_delivery = models.IntegerField()
    all_to_all = models.IntegerField(blank=True, null=True)
    include_email_in_csv = models.IntegerField()
    include_phone_in_csv = models.IntegerField()
    include_address1_in_csv = models.IntegerField()
    include_address2_in_csv = models.IntegerField()
    include_city_in_csv = models.IntegerField()
    include_state_in_csv = models.IntegerField()
    include_zip_in_csv = models.IntegerField()
    include_region_in_csv = models.IntegerField()
    include_postal_in_csv = models.IntegerField()
    include_country_in_csv = models.IntegerField()
    include_comment_in_csv = models.IntegerField()
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_petitiondeliveryjob"


class CorePetitionDeliveryJobPetitions(models.Model):
    """Joins the job to the page(s) to be delivered."""

    petitiondeliveryjob = models.ForeignKey(CorePetitionDeliveryJob, models.DO_NOTHING)
    page = models.ForeignKey(CorePage, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_petitiondeliveryjob_petitions"
        unique_together = (("petitiondeliveryjob", "page"),)


class CorePetitionDeliveryJobTargetGroups(models.Model):
    """Used to limit delivery to a subset of page targets."""

    petitiondeliveryjob = models.ForeignKey(CorePetitionDeliveryJob, models.DO_NOTHING)
    targetgroup_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_petitiondeliveryjob_target_groups"
        unique_together = (("petitiondeliveryjob", "targetgroup_id"),)


class CorePetitionPage(models.Model):
    """Page ID for all pages of type Petition and page specific attributes."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)
    send_immediate_fax = models.IntegerField(blank=True, null=True)
    send_immediate_email = models.IntegerField(blank=True, null=True)
    send_immediate_email_override_limit = models.IntegerField()
    email_mode = models.IntegerField(blank=True, null=True)
    remind_me_set_up_batch_delivery = models.IntegerField()
    immediate_email_subject = models.TextField(blank=True, null=True)
    delivery_template = models.TextField(blank=True, null=True)
    one_click = models.IntegerField()
    batch_delivery_from = models.ForeignKey(
        "CoreFromLine", models.DO_NOTHING, blank=True, null=True
    )
    batch_delivery_subject = models.CharField(max_length=255, blank=True, null=True)
    batch_delivery_template = models.TextField(blank=True, null=True)
    batch_petitiondeliveryjob_id = models.IntegerField(blank=True, null=True)
    send_immediate_email_delivery_blocked_at = models.DateTimeField(
        blank=True, null=True
    )
    batch_delivery_threshold = models.IntegerField(blank=True, null=True)
    batch_delivery_minimum = models.IntegerField()
    send_via_cwc = models.IntegerField(blank=True, null=True)
    cwc_topic = models.CharField(max_length=255, blank=True, null=True)
    cwc_statement = models.TextField(blank=True, null=True)
    cwc_subject = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_petitionpage"


class CorePetitionPageTargetGroups(models.Model):
    """Joins petition page to targets."""

    petitionpage = models.ForeignKey(CorePetitionPage, models.DO_NOTHING)
    targetgroup = models.ForeignKey("CoreTargetGroup", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_petitionpage_target_groups"
        unique_together = (("petitionpage", "targetgroup"),)


class CoreRecurringDonationCancelPage(models.Model):
    """Pointer to page id for all pages of type cancel recurring donation."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_recurringdonationcancelpage"


class CoreRecurringDonationUpdatePage(models.Model):
    """Pointer to page id for all pages of type update recurring donation."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "core_recurringdonationupdatepage"


class CoreSignupPage(models.Model):
    """Pointer to page id for all pages of type Signup."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_signuppage"


class CoreSurveyPage(models.Model):
    """Pointer to page id for all pages of type Survey."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_surveypage"


class CoreTag(models.Model):
    """Word or phrase which can be used to associate pages or emails with a campaign or issue."""

    name = models.CharField(unique=True, max_length=255)
    hidden = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    times_used = models.IntegerField(blank=True, null=True)
    order_index = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_tag"


class CoreTellAFriendPage(models.Model):
    """Pointer to page id for all tell-a-friend pages."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_tellafriendpage"


class CoreUnsubscribePage(models.Model):
    """Pointer to page id for all unsubscribe pages and user in mail wrapper flag."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)
    use_in_mail_wrapper = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_unsubscribepage"


class CoreUserUpdatePage(models.Model):
    """Pointer to page id for all user update pages."""

    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_userupdatepage"


class CoreWhipcountPage(models.Model):
    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_whipcountpage"


class CoreWhipcountPageTargetGroups(models.Model):
    """Joins whipcount page to targets."""

    whipcountpage = models.ForeignKey(CoreWhipcountPage, models.DO_NOTHING)
    targetgroup = models.ForeignKey("CoreTargetGroup", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_whipcountpage_target_groups"
        unique_together = (("whipcountpage", "targetgroup"),)


class CoreWhipcountPageFollowup(models.Model):
    pagefollowup_ptr = models.OneToOneField(
        CorePageFollowup, models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "core_whipcountpagefollowup"


# Target Tables
class CoreTarget(models.Model):
    """Contact information for the president, House and Senate members, and delegates, plus any custom targets you have added."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type = models.CharField(max_length=255)
    seat = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    us_district = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    long_title = models.CharField(max_length=255)
    first = models.CharField(max_length=255)
    last = models.CharField(max_length=255)
    official_full = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    fax = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    gender = models.CharField(max_length=1)
    party = models.CharField(max_length=255)
    hidden = models.IntegerField()
    district_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    twitter_id = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    youtube_id = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    instagram_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_target"


class CoreTargetGroup(models.Model):
    """Groups of targets."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    type = models.CharField(max_length=255)
    readonly = models.IntegerField()
    hidden = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_targetgroup"


class CoreBoundary(models.Model):
    """Unique geographic area defined by a spatial file or a handdrawn boundary. Can be associated with a custom target."""

    group_id = models.IntegerField()
    name = models.CharField(max_length=255)
    geometry = models.TextField()  # This field type is a guess.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_boundary"
        unique_together = (("group_id", "name"),)


class CoreBoundaryGroup(models.Model):
    """A group of boundaries of the same type (e.g. School District #23 boundary might belong to the Madison School District group)."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_boundarygroup"


class CoreCongressTargetGroup(models.Model):
    """Indicates whether the congressional group includes Republicans, Democrats, and/or Independents."""

    targetgroup_ptr = models.OneToOneField(
        CoreTargetGroup, models.DO_NOTHING, primary_key=True
    )
    include_republicans = models.IntegerField()
    include_democrats = models.IntegerField()
    include_independents = models.IntegerField()
    states = models.TextField()

    class Meta:
        managed = False
        db_table = "core_congresstargetgroup"


class CoreCongressTargetGroupExcludes(models.Model):
    """Individuals excluded from the congress target group above."""

    congresstargetgroup = models.ForeignKey(CoreCongressTargetGroup, models.DO_NOTHING)
    target = models.ForeignKey(CoreTarget, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_congresstargetgroup_excludes"
        unique_together = (("congresstargetgroup", "target"),)


class CoreCongressTargetGroupTargets(models.Model):
    """Individual legislators targeted (used when you pick specific individuals versus targeting by body and party)."""

    congresstargetgroup = models.ForeignKey(CoreCongressTargetGroup, models.DO_NOTHING)
    target = models.ForeignKey(CoreTarget, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_congresstargetgroup_targets"
        unique_together = (("congresstargetgroup", "target"),)


class CoreCwcDeliveryLog(models.Model):
    """Log of all successful constituent deliveries via the Communicating With Congress integration."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    target = models.ForeignKey(CoreTarget, models.DO_NOTHING)
    action = models.ForeignKey(CoreAction, models.DO_NOTHING)
    cwc_delivery_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_cwcdeliverylog"


class CoreCwcAvailableTargets(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    target = models.ForeignKey(CoreTarget, models.DO_NOTHING)
    office_code = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_cwcavailabletargets"


class CoreCwcRetryQueue(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    action = models.ForeignKey(CoreAction, models.DO_NOTHING)
    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    target = models.ForeignKey(CoreTarget, models.DO_NOTHING)
    retry_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_cwcretryqueue"


class CoreMediaTarget(models.Model):
    """Contact and circulation data for newspapers for LTEs."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    us_district = models.CharField(max_length=5)
    region = models.CharField(max_length=255)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    orgid = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    website_url = models.CharField(max_length=255, blank=True, null=True)
    circulation = models.IntegerField(blank=True, null=True)
    frequency = models.CharField(max_length=36, blank=True, null=True)
    language = models.CharField(max_length=64, blank=True, null=True)
    levelcode = models.CharField(max_length=64, blank=True, null=True)
    dmacode = models.CharField(max_length=10, blank=True, null=True)
    fipscode = models.IntegerField(blank=True, null=True)
    msacode = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_mediatarget"


class CorePageTargetChange(models.Model):
    """Used to redistribute signatures after a targeting change."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    targets_representation = models.TextField()

    class Meta:
        managed = False
        db_table = "core_pagetargetchange"


class CoreSpecialTargetGroup(models.Model):
    """A group of custom targets."""

    targetgroup_ptr = models.OneToOneField(
        CoreTargetGroup, models.DO_NOTHING, primary_key=True
    )
    jurisdiction = models.CharField(max_length=50)
    custom_boundaries = models.ForeignKey(
        CoreBoundaryGroup, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "core_specialtargetgroup"


class CoreSpecialTarget(models.Model):
    """Custom targets."""

    target_ptr = models.OneToOneField(CoreTarget, models.DO_NOTHING, primary_key=True)
    body = models.ForeignKey(CoreSpecialTargetGroup, models.DO_NOTHING)
    boundary_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_specialtarget"


class CorePolTarget(models.Model):
    """International targets."""

    target_ptr = models.OneToOneField(CoreTarget, models.DO_NOTHING, primary_key=True)
    body_id = models.CharField(max_length=255)
    person_id = models.CharField(max_length=255)
    division_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_poltarget"
        unique_together = (("body_id", "person_id"),)


class CorePolTargetGroup(models.Model):
    """A group of international targets."""

    targetgroup_ptr = models.OneToOneField(
        CoreTargetGroup, models.DO_NOTHING, primary_key=True
    )
    body_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_poltargetgroup"


class CoreTargetOffice(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    target = models.ForeignKey(CoreTarget, models.DO_NOTHING)
    type = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    fax = models.CharField(max_length=255)
    is_current = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_targetoffice"


# Event Tables
class EventsCampaign(models.Model):
    """Settings for a particular events campaign."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    title = models.CharField(max_length=255)
    name = models.CharField(unique=True, max_length=255)
    public_create_page = models.IntegerField()
    use_title = models.IntegerField()
    starts_at = models.DateTimeField(blank=True, null=True)
    use_start_date = models.IntegerField()
    use_start_time = models.IntegerField()
    require_staff_approval = models.IntegerField()
    require_email_confirmation = models.IntegerField()
    allow_private = models.IntegerField()
    max_event_size = models.IntegerField(blank=True, null=True)
    default_event_size = models.IntegerField(blank=True, null=True)
    public_search_page = models.IntegerField()
    show_title = models.IntegerField()
    show_venue = models.IntegerField()
    show_address1 = models.IntegerField()
    show_city = models.IntegerField()
    show_state = models.IntegerField()
    show_zip = models.IntegerField()
    show_public_description = models.IntegerField()
    show_directions = models.IntegerField()
    show_attendee_count = models.IntegerField()
    default_title = models.CharField(max_length=255)
    hidden = models.IntegerField()
    show_completed_events = models.IntegerField()
    show_full_events = models.IntegerField()
    timezone = models.CharField(max_length=255)
    allow_moderation = models.IntegerField()
    allow_moderator_edits = models.IntegerField(blank=True, null=True)
    show_notes = models.IntegerField(blank=True, null=True)
    mode_onsite = models.IntegerField()
    mode_local = models.IntegerField()
    mode_global = models.IntegerField()

    class Meta:
        managed = False
        db_table = "events_campaign"


class EventsCampaignVolunteer(models.Model):
    """Record of each volunteer moderator signup and their status."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)
    campaign = models.ForeignKey(EventsCampaign, models.DO_NOTHING)
    is_approved = models.IntegerField()
    status = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = "events_campaignvolunteer"


class EventsEmailBodyLog(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    body = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "events_emailbodylog"


class Event(models.Model):
    """Selections made by host for their event."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    us_district = models.CharField(max_length=5)
    region = models.CharField(max_length=255)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    campaign = models.ForeignKey(EventsCampaign, models.DO_NOTHING)
    title = models.CharField(max_length=255)
    creator = models.ForeignKey("CoreUser", models.DO_NOTHING)
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=32)
    host_is_confirmed = models.IntegerField()
    is_private = models.IntegerField()
    is_approved = models.IntegerField()
    attendee_count = models.IntegerField()
    max_attendees = models.IntegerField(blank=True, null=True)
    venue = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    public_description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    note_to_attendees = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    starts_at_utc = models.DateTimeField(blank=True, null=True)
    ends_at_utc = models.DateTimeField(blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    us_state_senate = models.CharField(max_length=6)
    us_state_district = models.CharField(max_length=6)
    merged_to = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)
    us_county = models.CharField(max_length=24, blank=True, null=True)
    mode = models.CharField(max_length=32)
    timezone = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "events_event"


class EventsEmailLog(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    from_type = models.CharField(max_length=32)
    to_type = models.CharField(max_length=32)
    event = models.ForeignKey(Event, models.DO_NOTHING)
    from_user = models.ForeignKey("CoreUser", models.DO_NOTHING, blank=True, null=True)
    from_admin = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    user_written_subject = models.TextField(blank=True, null=True)
    body = models.ForeignKey(EventsEmailBodyLog, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "events_emaillog"


class EventsEmailLogToUsers(models.Model):
    """Joins the email from the log to the recipient."""

    emaillog = models.ForeignKey(EventsEmailLog, models.DO_NOTHING)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "events_emaillog_to_users"
        unique_together = (("emaillog", "user"),)


class EventField(models.Model):
    """Custom event field -- host page."""

    parent = models.ForeignKey(Event, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = "events_eventfield"


class EventSignup(models.Model):
    """Record of each sign up, including role."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)
    event = models.ForeignKey(Event, models.DO_NOTHING)
    role = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    page_id = models.IntegerField()
    attended = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "events_eventsignup"
        unique_together = (("user", "event"),)


class EventSignupField(models.Model):
    """Custom event field -- attendee page."""

    parent = models.ForeignKey(EventSignup, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = "events_eventsignupfield"


class EventsHistoricalEvent(models.Model):
    """This stores previous versions of an event. Joins to events_event."""

    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    title = models.CharField(max_length=255)
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    starts_at_utc = models.DateTimeField(blank=True, null=True)
    ends_at_utc = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=32)
    host_is_confirmed = models.IntegerField()
    confirmed_at = models.DateTimeField(blank=True, null=True)
    is_private = models.IntegerField()
    is_approved = models.IntegerField()
    approved_at = models.DateTimeField(blank=True, null=True)
    attendee_count = models.IntegerField()
    max_attendees = models.IntegerField(blank=True, null=True)
    venue = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    us_district = models.CharField(max_length=5)
    region = models.CharField(max_length=255)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    us_state_senate = models.CharField(max_length=6)
    us_state_district = models.CharField(max_length=6)
    phone = models.CharField(max_length=255)
    public_description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    note_to_attendees = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    history_id = models.IntegerField()
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    campaign_id = models.IntegerField(blank=True, null=True)
    creator_id = models.IntegerField(blank=True, null=True)
    history_user_id = models.IntegerField(blank=True, null=True)
    merged_to_id = models.IntegerField(blank=True, null=True)
    us_county = models.CharField(max_length=24, blank=True, null=True)
    mode = models.CharField(max_length=32)
    timezone = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "events_historicalevent"


class EventsCustomEmailGroup(models.Model):
    """This associates a collection of custom event emails to a page. Joins to core_page."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    page = models.OneToOneField(CorePage, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "events_customemailgroup"


class EventsCustomEmail(models.Model):
    """Allows customizing an event's emails, like event approval and cancellation emails. Joins to events_customemailgroup."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    group = models.ForeignKey(EventsCustomEmailGroup, models.DO_NOTHING)
    email_subject = models.TextField(blank=True, null=True)
    email_body = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, db_collation="utf8mb3_general_ci")

    class Meta:
        managed = False
        db_table = "events_customemail"


# Donation Tables
class CoreAuthnetTransactionLog(models.Model):
    """Additional data from auth.net (empty unless they are your vendor)."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    source = models.CharField(max_length=255)
    raw = models.TextField()
    processed = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_authnettransactionlog"


class CoreCandidate(models.Model):
    """Candidates for use in bundling on donation pages."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(unique=True, max_length=255)
    fec_id = models.CharField(unique=True, max_length=16, blank=True, null=True)
    portrait_url = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255)
    is_ours = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_candidate"


class CoreCandidateTags(models.Model):
    """Tags associated with a candidate."""

    candidate = models.ForeignKey(CoreCandidate, models.DO_NOTHING)
    tag = models.ForeignKey(CoreTag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_candidate_tags"
        unique_together = (("candidate", "tag"),)


class CoreOrderUserDetail(models.Model):
    """Billing information for user and source of action. Billing address is the last saved address for the order. Updates to the billing address for a recurring profile made by the user or an admin will overwrite the previously saved billing address in this table."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(max_length=255)
    prefix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    source = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_order_user_detail"


class CoreOrderShippingAddress(models.Model):
    """Shipping address for orders of shippable products."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_order_shipping_address"


class CoreOrder(models.Model):
    """Information about donations and/or product orders made by a user."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    action = models.OneToOneField(CoreAction, models.DO_NOTHING)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)
    user_detail = models.ForeignKey(CoreOrderUserDetail, models.DO_NOTHING)
    shipping_address = models.ForeignKey(
        CoreOrderShippingAddress, models.DO_NOTHING, blank=True, null=True
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    total_converted = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255)
    card_num_last_four = models.CharField(max_length=4, blank=True, null=True)
    import_id = models.CharField(max_length=64, blank=True, null=True)
    account = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_order"
        unique_together = (("import_id", "account"),)


class CoreOrderRecurring(models.Model):
    """Information about recurring donation commitments made by a user."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    order = models.OneToOneField(CoreOrder, models.DO_NOTHING)
    action = models.OneToOneField(CoreAction, models.DO_NOTHING)
    exp_date = models.CharField(max_length=6)
    card_num = models.CharField(max_length=4)
    recurring_id = models.CharField(max_length=255, blank=True, null=True)
    account = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)
    start = models.DateField()
    period = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    amount_converted = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_orderrecurring"


class CoreTransaction(models.Model):
    """Transactions are created for every donation processed through ActionKit."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type = models.CharField(max_length=255)
    order = models.ForeignKey(CoreOrder, models.DO_NOTHING)
    account = models.CharField(max_length=255)
    test_mode = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_converted = models.DecimalField(max_digits=10, decimal_places=2)
    success = models.IntegerField()
    trans_id = models.CharField(max_length=255, blank=True, null=True)
    failure_description = models.TextField(blank=True, null=True)
    failure_code = models.CharField(max_length=255, blank=True, null=True)
    failure_message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255)
    currency = models.CharField(max_length=3)
    ref_transaction = models.ForeignKey(
        "self", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "core_transaction"


class CoreDonationChangeLog(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    change_type = models.CharField(max_length=255)
    action = models.ForeignKey(CoreAction, models.DO_NOTHING)
    order = models.ForeignKey(CoreOrder, models.DO_NOTHING)
    recurring = models.ForeignKey(
        CoreOrderRecurring, models.DO_NOTHING, blank=True, null=True
    )
    transaction = models.ForeignKey(
        CoreTransaction, models.DO_NOTHING, blank=True, null=True
    )
    new_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING, blank=True, null=True)
    staff = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_donationchangelog"


class CoreDonationHpcRule(models.Model):
    """Name and timestamps for each set of rules for suggested ask amounts based on HPC (Highest Previous Contribution), 2nd highest contribution, and average."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    hidden = models.IntegerField()
    which_amount = models.CharField(max_length=255)
    timespan = models.CharField(max_length=255)
    currency = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = "core_donation_hpc_rule"


class CoreDonationHpcRuleCondition(models.Model):
    """Thresholds and ask amounts for each set of Suggestion Ask Rules."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    rule = models.ForeignKey(CoreDonationHpcRule, models.DO_NOTHING)
    threshold = models.CharField(max_length=10)
    ask = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "core_donation_hpc_rule_condition"


class CoreDonationHpcRuleExcludeTags(models.Model):
    """Joins tags you've selected for exclusion from suggested ask rules with the rule."""

    donationhpcrule = models.ForeignKey(CoreDonationHpcRule, models.DO_NOTHING)
    tag = models.ForeignKey(CoreTag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_donation_hpc_rule_exclude_tags"
        unique_together = (("donationhpcrule", "tag"),)


class CoreDonationFraudFilter(models.Model):
    """MaxMind anti-fraud settings which apply if you enable this."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(unique=True, max_length=255)
    check_maxmind = models.IntegerField()
    maxmind_threshold = models.IntegerField()
    whitelist_where = models.TextField()
    blacklist_where = models.TextField()
    is_default_for_mailings = models.IntegerField()
    is_default_for_web = models.IntegerField()
    message = models.TextField()

    class Meta:
        managed = False
        db_table = "core_donationfraudfilter"


class CoreDonationpageCandidates(models.Model):
    """Joins donation page to candidate."""

    donationpage = models.ForeignKey(CoreDonationPage, models.DO_NOTHING)
    candidate = models.ForeignKey(CoreCandidate, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_donationpage_candidates"
        unique_together = (("donationpage", "candidate"),)


class CoreProduct(models.Model):
    """Name, price and other key information for products to be used on donation pages."""

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    shippable = models.IntegerField()
    status = models.CharField(max_length=255)
    maximum_order = models.IntegerField()
    hidden = models.IntegerField()
    admin_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_product"
        unique_together = (("name", "admin_name"),)


class CoreDonationpageProducts(models.Model):
    """Joins donation page to product."""

    donationpage = models.ForeignKey(CoreDonationPage, models.DO_NOTHING)
    product = models.ForeignKey(CoreProduct, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_donationpage_products"
        unique_together = (("donationpage", "product"),)


class CoreOrderDetail(models.Model):
    """Quantity and amount of products ordered by a user."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    order = models.ForeignKey(CoreOrder, models.DO_NOTHING)
    product = models.ForeignKey(CoreProduct, models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_converted = models.DecimalField(max_digits=10, decimal_places=2)
    candidate = models.ForeignKey(
        CoreCandidate, models.DO_NOTHING, blank=True, null=True
    )
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_order_detail"


class CorePaymentAccount(models.Model):
    """Configuration information for payment accounts"""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(unique=True, max_length=255)
    processor = models.CharField(max_length=255)
    auth = models.TextField()
    extra = models.JSONField()

    class Meta:
        managed = False
        db_table = "core_paymentaccount"


class CoreProductTags(models.Model):
    """Associates a product with a tag or tags."""

    product = models.ForeignKey(CoreProduct, models.DO_NOTHING)
    tag = models.ForeignKey(CoreTag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_product_tags"
        unique_together = (("product", "tag"),)


# Mailing Tables
class CoreFromLine(models.Model):
    """Names and email addresses from which emails can be sent."""

    from_line = models.TextField(blank=True, null=True)
    hidden = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_default = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_fromline"


class CoreEmailWrapper(models.Model):
    """Sets the appearance of an email."""

    name = models.CharField(unique=True, max_length=255)
    template = models.TextField()
    text_template = models.TextField()
    hidden = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    unsubscribe_text = models.TextField(blank=True, null=True)
    unsubscribe_html = models.TextField(blank=True, null=True)
    is_default = models.IntegerField(blank=True, null=True)
    lang = models.ForeignKey(CoreLanguage, models.DO_NOTHING, blank=True, null=True)
    amp_template = models.TextField(blank=True, null=True)
    unsubscribe_amp_html = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_emailwrapper"


class CoreMailboxProviderActivity(models.Model):
    """Matches users based on their recent engagement history and mailbox provider, in order to allow you to target mailings. This is commonly used to target active users or exclude inactive users."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    criteria = models.JSONField()
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=16)
    hidden = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_mailboxprovideractivity"


class CoreMailingTargeting(models.Model):
    """Criteria for inclusion or exclusion from the select recipients screen. Joins to core_mailing on core_mailingtargeting.id=core_mailing.includes_id or core_mailing.excludes_id."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    states = models.TextField(blank=True, null=True)
    cds = models.TextField(blank=True, null=True)
    zips = models.TextField(blank=True, null=True)
    zip_radius = models.IntegerField(blank=True, null=True)
    has_donated = models.IntegerField(blank=True, null=True)
    is_monthly_donor = models.IntegerField(blank=True, null=True)
    raw_sql = models.TextField(blank=True, null=True)
    state_house_districts = models.TextField(blank=True, null=True)
    state_senate_districts = models.TextField(blank=True, null=True)
    is_delivery = models.IntegerField(blank=True, null=True)
    delivery_job = models.ForeignKey(
        CorePetitionDeliveryJob, models.DO_NOTHING, blank=True, null=True
    )
    counties = models.TextField(blank=True, null=True)
    campaign_radius = models.IntegerField(blank=True, null=True)
    countries = models.TextField(blank=True, null=True)
    divisions = models.TextField(blank=True, null=True)
    campaign_samestate_only = models.IntegerField()
    mirror_mailing_excludes = models.IntegerField()
    regions = models.TextField(blank=True, null=True)
    campaign_same_district_only = models.IntegerField()
    campaign_first_date = models.CharField(max_length=16, blank=True, null=True)
    campaign_last_date = models.CharField(max_length=16, blank=True, null=True)
    campaign_same_county_only = models.IntegerField()
    scorepool_score_min = models.IntegerField(blank=True, null=True)
    scorepool_score_max = models.IntegerField(blank=True, null=True)
    scorepool_score_include_missing = models.IntegerField()
    mailbox_provider_activity = models.ForeignKey(
        CoreMailboxProviderActivity, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "core_mailingtargeting"


class CoreMergeFile(models.Model):
    """Merge files uploaded for use in mailings."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    status = models.CharField(max_length=20, blank=True, null=True)
    lookup_table = models.CharField(max_length=255, blank=True, null=True)
    lookup_column = models.CharField(max_length=255, blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    row_count = models.IntegerField(blank=True, null=True)
    line_count = models.IntegerField(blank=True, null=True)
    error = models.TextField()
    s3_bucket = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_mergefile"


class CoreMailingTestGroup(models.Model):
    """A group of mailings for launching and viewing test results together."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    title = models.TextField(blank=True, null=True)
    prime = models.IntegerField()
    number_of_mailings = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_mailingtestgroup"


class CoreMailing(models.Model):
    """Content and key information for all sent and draft emails."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    fromline = models.ForeignKey(CoreFromLine, models.DO_NOTHING, blank=True, null=True)
    custom_fromline = models.TextField(blank=True, null=True)
    reply_to = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    lang = models.ForeignKey(CoreLanguage, models.DO_NOTHING, blank=True, null=True)
    emailwrapper = models.ForeignKey(
        CoreEmailWrapper, models.DO_NOTHING, blank=True, null=True
    )
    web_viewable = models.IntegerField(blank=True, null=True)
    landing_page = models.ForeignKey(
        "CorePage", models.DO_NOTHING, blank=True, null=True
    )
    winning_subject = models.ForeignKey(
        "CoreMailingSubject", models.DO_NOTHING, blank=True, null=True
    )
    requested_proofs = models.IntegerField(blank=True, null=True)
    submitter = models.ForeignKey(
        AuthUser,
        models.DO_NOTHING,
        related_name="mailing_submitted",
        blank=True,
        null=True,
    )
    queue_task_id = models.CharField(max_length=255, blank=True, null=True)
    queued_at = models.DateTimeField(blank=True, null=True)
    queued_by = models.ForeignKey(
        AuthUser,
        models.DO_NOTHING,
        related_name="mailing_queued",
        blank=True,
        null=True,
    )
    expected_send_count = models.IntegerField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    query_queued_at = models.DateTimeField(blank=True, null=True)
    query_started_at = models.DateTimeField(blank=True, null=True)
    query_completed_at = models.DateTimeField(blank=True, null=True)
    query_previous_runtime = models.IntegerField(blank=True, null=True)
    query_status = models.CharField(max_length=255, blank=True, null=True)
    query_task_id = models.CharField(max_length=255, blank=True, null=True)
    targeting_version = models.IntegerField(blank=True, null=True)
    targeting_version_saved = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    includes = models.ForeignKey(
        CoreMailingTargeting,
        models.DO_NOTHING,
        related_name="mailing_includes",
        blank=True,
        null=True,
    )
    excludes = models.ForeignKey(
        CoreMailingTargeting,
        models.DO_NOTHING,
        related_name="mailing_excludes",
        blank=True,
        null=True,
    )
    limit = models.IntegerField(blank=True, null=True)
    sort_by = models.CharField(max_length=32, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)
    pid = models.IntegerField(blank=True, null=True)
    hidden = models.IntegerField()
    target_group_from_landing_page = models.IntegerField()
    scheduled_for = models.DateTimeField(blank=True, null=True)
    scheduled_by = models.ForeignKey(
        AuthUser,
        models.DO_NOTHING,
        related_name="mailing_scheduled",
        blank=True,
        null=True,
    )
    sent_proofs = models.IntegerField()
    rebuild_query_at_send = models.IntegerField()
    limit_percent = models.IntegerField(blank=True, null=True)
    mergefile = models.ForeignKey(
        CoreMergeFile, models.DO_NOTHING, blank=True, null=True
    )
    target_mergefile = models.IntegerField()
    mails_per_second = models.FloatField(blank=True, null=True)
    recurring_schedule = models.ForeignKey(
        "CoreRecurringMailingSchedule", models.DO_NOTHING, blank=True, null=True
    )
    recurring_source_mailing = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        related_name="mailing_recurring_source",
        blank=True,
        null=True,
    )
    requested_proof_date = models.DateTimeField(blank=True, null=True)
    send_date = models.CharField(max_length=255)
    exclude_ordering = models.IntegerField(blank=True, null=True)
    test_group = models.ForeignKey(
        CoreMailingTestGroup, models.DO_NOTHING, blank=True, null=True
    )
    test_remainder = models.IntegerField(blank=True, null=True)
    mergequery_report = models.ForeignKey(
        "ReportsQueryReport", models.DO_NOTHING, blank=True, null=True
    )
    target_mergequery = models.IntegerField()
    send_time_source = models.CharField(max_length=64, blank=True, null=True)
    send_time_validation_job = models.ForeignKey(
        "CoreJob", models.DO_NOTHING, blank=True, null=True
    )
    version = models.SmallIntegerField()
    archive = models.TextField(blank=True, null=True)
    use_autotest = models.IntegerField()
    autotest_status = models.CharField(max_length=255, blank=True, null=True)
    autotest_resend = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        related_name="mailing_autotest_resend",
        blank=True,
        null=True,
    )
    autotest_wait_minutes = models.IntegerField(blank=True, null=True)
    autotest_metric = models.CharField(max_length=32, blank=True, null=True)
    autotest_max_unsub_rate = models.FloatField(blank=True, null=True)
    send_time_local = models.DateTimeField(blank=True, null=True)
    send_time_local_fallback = models.DateTimeField(blank=True, null=True)
    amp_html = models.TextField(blank=True, null=True)
    send_time_local_no_fallback = models.IntegerField(blank=True, null=True)
    bee_json = models.TextField(
        db_collation="utf8mb4_unicode_ci", blank=True, null=True
    )
    bee_session = models.CharField(max_length=36, blank=True, null=True)
    amp_archive = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_mailing"


class CoreAllowedEmailWrapperField(models.Model):
    """Field created by your group to customize settings in your email wrapper. Similar to templateset fields, but for email wrappers."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    order_index = models.IntegerField()
    display_name = models.CharField(unique=True, max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    always_show = models.IntegerField()
    required = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    field_type = models.CharField(max_length=32)
    field_default = models.TextField()
    field_choices = models.TextField()
    field_regex = models.TextField()
    field_length = models.IntegerField(blank=True, null=True)
    allow_multiple = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_allowedemailwrapperfield"


class CoreAllowedMailingField(models.Model):
    """Field created by your group to customize settings in your mailing."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(
        primary_key=True, max_length=255, db_collation="utf8mb3_general_ci"
    )
    always_show = models.IntegerField()
    display_name = models.CharField(unique=True, max_length=255)
    order_index = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    field_default = models.TextField()
    field_choices = models.TextField()
    field_regex = models.TextField()
    field_type = models.CharField(max_length=32, db_collation="utf8mb3_general_ci")
    field_length = models.IntegerField(blank=True, null=True)
    required = models.IntegerField()
    allow_multiple = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_allowedmailingfield"


class CoreBlackholedDomain(models.Model):
    """List of email domains to suppress from bulk and transactional mailings."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    domain = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = "core_blackholeddomain"


class CoreBlackholedEmail(models.Model):
    """List of email addresses to suppress from bulk and transactional mailings."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = "core_blackholedemail"


class CoreBlackholedHistory(models.Model):
    """Log of all email addresses that were suppressed from bulk or transactional mailings, along with mailing_id or action_id if available."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(max_length=255)
    mailing_id = models.IntegerField(blank=True, null=True)
    action_id = models.IntegerField(blank=True, null=True)
    matched_email = models.IntegerField()
    matched_domain = models.IntegerField()
    matched_pattern = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_blackholedhistory"


class CoreBlackholedPattern(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    pattern = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = "core_blackholedpattern"


class CoreBounce(models.Model):
    """User and mailing id for all hard bounces. Bounced users are unsubscribed."""

    user_id = models.IntegerField()
    mailing_id = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField()
    action_id = models.IntegerField(blank=True, null=True)
    bounce_type = models.CharField(max_length=6, blank=True, null=True)
    bounce_class = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_bounce"
        unique_together = (
            ("user_id", "action_id"),
            ("user_id", "mailing_id"),
        )


class CoreBounceSoft(models.Model):
    """User and mailing id for soft bounces that get recorded by ActionKit."""

    user_id = models.IntegerField()
    mailing_id = models.IntegerField(blank=True, null=True)
    action_id = models.IntegerField(blank=True, null=True)
    bounce_class = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_bounce_soft"
        unique_together = (
            ("user_id", "mailing_id"),
            ("user_id", "action_id"),
        )


class CoreClick(models.Model):
    """Tracks clicks to a page. Only clicks with a mailing_id are associated with a mailing."""

    clickurl_id = models.IntegerField()
    user_id = models.IntegerField(blank=True, null=True)
    mailing_id = models.IntegerField(blank=True, null=True)
    link_number = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    referring_user_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    useragent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_click"


class CoreClickRaw(models.Model):
    """As core_click, but tracks clicks to a page, which includes real clicks and those believed to be created by software or email providers hiding actual user activity. Only clicks with a mailing_id are associated with a mailing. Raw clicks older than 90 days are deleted automatically."""

    id = models.BigAutoField(primary_key=True)
    clickurl_id = models.IntegerField()
    user_id = models.IntegerField(blank=True, null=True)
    mailing_id = models.IntegerField(blank=True, null=True)
    link_number = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    referring_user_id = models.IntegerField(blank=True, null=True)
    useragent_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_click_raw"


class CoreClickUrl(models.Model):
    """Relates url for click tracking to the page."""

    url = models.CharField(unique=True, max_length=255)
    page = models.ForeignKey(CorePage, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_clickurl"


class CoreClientDomain(models.Model):
    """Other domains you control and for which links in emails should be tracked as ActionKit domains."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    domain = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = "core_clientdomain"


class CoreEmailTemplate(models.Model):
    name = models.CharField(unique=True, max_length=255)
    wrapper = models.ForeignKey(CoreEmailWrapper, models.DO_NOTHING)
    from_line = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    template = models.TextField()

    class Meta:
        managed = False
        db_table = "core_emailtemplate"


class CoreFileAttachment(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)
    action = models.ForeignKey(CoreAction, models.DO_NOTHING)
    field_type = models.CharField(max_length=8)
    field_name = models.CharField(max_length=255)
    file_url = models.CharField(max_length=1024)
    bucket = models.CharField(max_length=255)
    directory = models.CharField(max_length=255)
    unique_id = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_fileattachment"


class CoreEmailWrapperField(models.Model):
    """Custom email wrapper field value. Joins to core_emailwrapper."""

    parent = models.ForeignKey(CoreEmailWrapper, models.DO_NOTHING)
    name = models.ForeignKey(
        CoreAllowedEmailWrapperField, models.DO_NOTHING, db_column="name"
    )
    value = models.TextField()

    class Meta:
        managed = False
        db_table = "core_emailwrapperfield"


class CoreMailingSubject(models.Model):
    """Subject or subjects associated with an email"""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    text = models.TextField(blank=True, null=True)
    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)
    preview_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_mailingsubject"


class CoreFailedUserMailing(models.Model):
    """Record of mailings where a user was targeted but not sent an email because of a missing or bad snippet value."""

    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)
    user_id = models.IntegerField()
    subject = models.ForeignKey(
        CoreMailingSubject, models.DO_NOTHING, blank=True, null=True
    )
    created_at = models.DateTimeField()
    reason = models.TextField()

    class Meta:
        managed = False
        db_table = "core_failedusermailing"
        unique_together = (("mailing", "user_id"),)


class CoreMailingProofUsers(models.Model):
    """Shows user_ids entered under "see proofs for specific users" and the mailing_id."""

    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailing_proof_users"
        unique_together = (("mailing", "user"),)


class CoreMailingReviewers(models.Model):
    """Shows which mailings were sent as proofs to which staff users."""

    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailing_reviewers"
        unique_together = (("mailing", "user"),)


class CoreMailingTags(models.Model):
    """Associates a mailing with a tag."""

    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)
    tag = models.ForeignKey(CoreTag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailing_tags"
        unique_together = (("mailing", "tag"),)


class CoreMailingError(models.Model):
    """Information that may be helpful in identifying the cause of a mailing error."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)
    queue_task_id = models.CharField(max_length=255)
    traceback = models.TextField()

    class Meta:
        managed = False
        db_table = "core_mailingerror"


class CoreMailingField(models.Model):
    """Custom mailing field value. Joins to core_mailing."""

    parent = models.ForeignKey(CoreMailing, models.DO_NOTHING)
    name = models.ForeignKey(
        CoreAllowedMailingField, models.DO_NOTHING, db_column="name"
    )
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_mailingfield"


class CoreMailingHaiku(models.Model):
    """Mailer haikus."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    text = models.TextField()

    class Meta:
        managed = False
        db_table = "core_mailinghaiku"


class CoreMailingTargetingBoundaries(models.Model):
    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    boundary_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_boundaries"
        unique_together = (("mailingtargeting", "boundary_id"),)


class CoreMailingTargetingBoundaryGroups(models.Model):
    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    boundarygroup = models.ForeignKey(CoreBoundaryGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_boundary_groups"
        unique_together = (("mailingtargeting", "boundarygroup"),)


class CoreMailingTargetingMailboxProviderActivity(models.Model):
    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    mailboxprovideractivity = models.ForeignKey(
        CoreMailboxProviderActivity, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_mailbox_provider_activity"
        unique_together = (("mailingtargeting", "mailboxprovideractivity"),)


class CoreMailingTargetingMessages(models.Model):
    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    message = models.ForeignKey("TextingMessage", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_messages"
        unique_together = (("mailingtargeting", "message"),)


class CoreMailingVariation(models.Model):
    """The variations of an A/B mailing test."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)
    letter = models.CharField(max_length=2)
    notes = models.CharField(max_length=255, blank=True, null=True)
    archive = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_mailingvariation"
        unique_together = (("mailing", "letter"),)


class CoreMailingVariationUsers(models.Model):
    """Mapping between A/B test variations and the users who received them."""

    mailingvariation = models.ForeignKey(CoreMailingVariation, models.DO_NOTHING)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingvariation_users"
        unique_together = (("mailingvariation", "user"),)


class CoreMailingVariationDetail(models.Model):
    """The content changes for variations in A/B mailing tests. The built-in fields are treated as variation A and all other variations are here."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    variation = models.ForeignKey(CoreMailingVariation, models.DO_NOTHING)
    field_type = models.CharField(max_length=255)
    field_name = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = "core_mailingvariationdetail"


class CoreMailingTargetingActions(models.Model):
    """Targeting by whether user has taken action on a given page. Additional criteria (for inclusion or exclusion) added to set defined in core_mailingtargeting."""

    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    page = models.ForeignKey(CorePage, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_actions"
        unique_together = (("mailingtargeting", "page"),)


class CoreMailingtargetingCampaigns(models.Model):
    """Targeting users by proximity (specified in core_mailingtargeting) to event in the campaign in this table."""

    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    campaign = models.ForeignKey(EventsCampaign, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_campaigns"
        unique_together = (("mailingtargeting", "campaign"),)


class CoreMailingTargetingLanguages(models.Model):
    """Targeting by whether user took action on a page associated with the given language."""

    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    language = models.ForeignKey(CoreLanguage, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_languages"
        unique_together = (("mailingtargeting", "language"),)


class CoreMailingTargetingLists(models.Model):
    """Targeting by whether user is on a given list."""

    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    list = models.ForeignKey("CoreList", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_lists"
        unique_together = (("mailingtargeting", "list"),)


class CoreMailingTargetingMailings(models.Model):
    """Targeting by whether user is included in the targeting for another mailing."""

    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_mailings"
        unique_together = (("mailingtargeting", "mailing"),)


class CoreMailingTargetingTags(models.Model):
    """Targeting by whether the user took action on a page associated with the designated tag."""

    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    tag = models.ForeignKey("CoreTag", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_tags"
        unique_together = (("mailingtargeting", "tag"),)


class CoreMailingTargetingTargetGroups(models.Model):
    """Targeting constituents of advocacy targets in specified target group (as defined from links on the pages tab)."""

    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    targetgroup = models.ForeignKey(CoreTargetGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_target_groups"
        unique_together = (("mailingtargeting", "targetgroup"),)


class CoreMailingtargetingUserGroups(models.Model):
    """Targeting by usergroup_id."""

    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    usergroup = models.ForeignKey("CoreUserGroup", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_user_groups"
        unique_together = (("mailingtargeting", "usergroup"),)


class CoreMailingTargetingUsers(models.Model):
    """Targeting by user_id."""

    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_users"
        unique_together = (("mailingtargeting", "user"),)


class CoreRecurringDonorTargetingOption(models.Model):
    """Recurring donor statuses available in mailer targeting "Monthly Donors" box."""

    code = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_recurringdonortargetingoption"


class CoreMailingTargetingWasMonthlyDonor(models.Model):
    """Targeting by recurring donor status. Joins to core_recurringdonortargetingoption."""

    mailingtargeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    recurringdonortargetingoption = models.ForeignKey(
        CoreRecurringDonorTargetingOption, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "core_mailingtargeting_was_monthly_donor"
        unique_together = (("mailingtargeting", "recurringdonortargetingoption"),)


class CoreMailingTargetingSummary(models.Model):
    """Statistics about this mailing set's users, frozen at the time of the mailing set build. Uses summary_user in order to calculate all stats. All data should be interpreted in the context of when the mailing was built. Can be compared with core_userdailysummary when the created_at dates of both are equal to determine whether this mailing set is average, better than average, or worse than average."""

    mailing = models.OneToOneField(CoreMailing, models.DO_NOTHING, primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    targeting_version = models.IntegerField(blank=True, null=True)
    avg_last_mailed = models.IntegerField(blank=True, null=True)
    avg_last_open = models.IntegerField(blank=True, null=True)
    avg_last_click = models.IntegerField(blank=True, null=True)
    avg_last_mailing_action = models.IntegerField(blank=True, null=True)
    avg_last_donation = models.IntegerField(blank=True, null=True)
    avg_actions_last_90_days = models.IntegerField(blank=True, null=True)
    avg_scorepool_userscore = models.IntegerField(blank=True, null=True)
    users_without_summary = models.IntegerField(blank=True, null=True)
    users_without_last_mailed = models.IntegerField(blank=True, null=True)
    users_without_last_open = models.IntegerField(blank=True, null=True)
    users_without_last_click = models.IntegerField(blank=True, null=True)
    users_without_last_mailing_action = models.IntegerField(blank=True, null=True)
    users_without_last_donation = models.IntegerField(blank=True, null=True)
    users_without_scorepool_userscore = models.IntegerField(blank=True, null=True)
    recipients = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_mailingtargetingsummary"


class CoreMailingAdditionalTargeting(models.Model):
    """Associates additional targeting sets with a mailing for OR targeting functionality."""

    mailingtargeting_ptr = models.OneToOneField(
        CoreMailingTargeting, models.DO_NOTHING, primary_key=True
    )
    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_mailingadditionaltargeting"


class CoreMergeQueryParam(models.Model):
    """Parameters to use with the merge query for a specific mailing."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_mergequeryparam"


class CoreMessageEventRaw(models.Model):
    """Stores the last 90 days of raw deliverability data, such as bounces and delays."""

    user_id = models.IntegerField(blank=True, null=True)
    mailing_id = models.IntegerField(blank=True, null=True)
    action_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    timestamp = models.DateTimeField(blank=True, null=True)
    event_type = models.CharField(max_length=25)
    bounce_class = models.IntegerField(blank=True, null=True)
    smtp_error_code = models.CharField(max_length=3, blank=True, null=True)
    ext_event_id = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = "core_message_event_raw"
        unique_together = (("id", "created_at"),)


class CoreOpen(models.Model):
    """Tracks all real opens by mailing and user."""

    user_id = models.IntegerField(blank=True, null=True)
    mailing_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    useragent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_open"


class CoreOpenRaw(models.Model):
    """As core_open, but tracks all opens by mailing and user, which includes real opens and those believed to be created by software or email providers hiding actual user activity. Raw opens older than 90 days are deleted automatically."""

    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    mailing_id = models.IntegerField(blank=True, null=True)
    useragent_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_open_raw"
        unique_together = (("id", "created_at"),)


class CoreOpenRawOld(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    mailing_id = models.IntegerField(blank=True, null=True)
    useragent_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_open_raw_old"
        unique_together = (("id", "created_at"),)


class CoreQueuedEmail(models.Model):
    envelope_sender = models.TextField()
    to = models.TextField()
    message = models.TextField()
    metadata = models.TextField()

    class Meta:
        managed = False
        db_table = "core_queuedemail"


class CoreRecurringMailingSchedule(models.Model):
    """Table for storage of recurring series information."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(max_length=255)
    tz_name = models.CharField(max_length=64)
    schedule_type = models.CharField(max_length=255, blank=True, null=True)
    hours = models.CharField(max_length=255, blank=True, null=True)
    days_of_week = models.CharField(max_length=255, blank=True, null=True)
    days_of_month = models.CharField(max_length=255, blank=True, null=True)
    send_finished_notice = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_recurringmailingschedule"


class CoreRedirect(models.Model):
    """See short links section of user guide."""

    short_code = models.CharField(unique=True, max_length=255, blank=True, null=True)
    url = models.CharField(max_length=4096, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_redirect"


class CoreTargetingActionField(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    targeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    page = models.ForeignKey(CorePage, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    values = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_targetingactionfield"


class CoreTargetingQueryReport(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    report = models.ForeignKey("ReportsQueryReport", models.DO_NOTHING)
    targeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_targetingqueryreport"


class CoreTargetingQueryReportParam(models.Model):
    """Additional parameters provided by staffer when using a query report to target a mailing."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    query = models.ForeignKey(CoreTargetingQueryReport, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=4096, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_targetingqueryreportparam"


class CoreTargetingUserField(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    targeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    field = models.ForeignKey("CoreAllowedUserField", models.DO_NOTHING)
    values = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_targetinguserfield"


class CoreUserDailySummary(models.Model):
    """Statistics about your subscribed users who have a record in summary_user and have received at least 1 mailing in the last 30 days. Uses summary_user in order to calculate all stats. All data should be interpreted in the context of when the record was created. Can be compared with core_mailingtargetingsummary when the created_at dates of both are equal to determine whether that mailing set is average, better than average, or worse than average."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    avg_last_mailed = models.IntegerField(blank=True, null=True)
    avg_last_open = models.IntegerField(blank=True, null=True)
    avg_last_click = models.IntegerField(blank=True, null=True)
    avg_last_mailing_action = models.IntegerField(blank=True, null=True)
    avg_last_donation = models.IntegerField(blank=True, null=True)
    avg_actions_last_90_days = models.IntegerField(blank=True, null=True)
    avg_scorepool_userscore = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_userdailysummary"


class CoreUserMailing(models.Model):
    """Record of every mailing sent to every user."""

    id = models.BigAutoField(primary_key=True)
    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)
    subject = models.ForeignKey(
        CoreMailingSubject, models.DO_NOTHING, blank=True, null=True
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_usermailing"
        unique_together = (("mailing", "user"),)


class CoreAmpTap(models.Model):
    """Records when AMP Emails are clicked/tapped."""

    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    user_id = models.IntegerField(blank=True, null=True)
    mailing_id = models.IntegerField(blank=True, null=True)
    useragent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_amptap"


# Transactional Mailing Tables
class CoreTransactionalMailing(models.Model):
    """Content and key information for all sent transactional emails."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    wrapper = models.ForeignKey(
        CoreEmailWrapper, models.DO_NOTHING, blank=True, null=True
    )
    from_line = models.ForeignKey(
        CoreFromLine, models.DO_NOTHING, blank=True, null=True
    )
    custom_from = models.CharField(max_length=255)
    reply_to = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20)
    signature = models.CharField(max_length=255, blank=True, null=True)
    variation = models.ForeignKey(
        "LabVariation", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "core_transactionalmailing"


class CoreNotificationMailing(models.Model):
    """Records every action notification mailing and joins to core_transactionalmailing."""

    transactionalmailing_ptr = models.OneToOneField(
        CoreTransactionalMailing, models.DO_NOTHING, primary_key=True
    )
    notification = models.ForeignKey(CoreActionNotification, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_notificationmailing"


class CoreTafMailing(models.Model):
    """Records every tell-a-friend mailing sent through ActionKit and joins to core_transactionalmailing."""

    transactionalmailing_ptr = models.OneToOneField(
        CoreTransactionalMailing, models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "core_tafmailing"


class CoreConfirmationMailing(models.Model):
    """Records every confirmation mailing and joins to core_transactionalmailing."""

    transactionalmailing_ptr = models.OneToOneField(
        CoreTransactionalMailing, models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "core_confirmationmailing"


class CoreConfirmationMailingBody(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    confirmation_mailing_id = models.IntegerField()
    action_id = models.IntegerField()
    body = models.TextField()
    subject = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_confirmationmailingbody"


class CoreTransactionalMailingSent(models.Model):
    """The core_transactionalmailingsent table stores a row each time a transactional mailing is sent."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    action = models.ForeignKey(CoreAction, models.DO_NOTHING)
    transactional_mailing = models.ForeignKey(
        CoreTransactionalMailing, models.DO_NOTHING
    )
    user = models.ForeignKey("CoreUser", models.DO_NOTHING, blank=True, null=True)
    email = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_transactionalmailingsent"


class CoreTransactionalMailingAction(models.Model):
    """The core_transactionalmailingaction table stores a row each time a user takes action after clicking on a transactional mailing link."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    transactional_mailing_sent = models.ForeignKey(
        CoreTransactionalMailingSent, models.DO_NOTHING
    )
    action = models.ForeignKey(CoreAction, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_transactionalmailingaction"


class CoreTransactionalMailingClick(models.Model):
    """The core_transactionalmailingclick table stores a row each time a transactional mailing is clicked."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    transactional_mailing_sent = models.ForeignKey(
        CoreTransactionalMailingSent, models.DO_NOTHING
    )
    clickurl = models.ForeignKey(CoreClickUrl, models.DO_NOTHING)
    link_number = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_transactionalmailingclick"


class CoreTransactionalMailingOpen(models.Model):
    """The core_transactionalmailingopen table stores a row each time a transactional mailing is opened."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    transactional_mailing_sent = models.ForeignKey(
        CoreTransactionalMailingSent, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "core_transactionalmailingopen"


class CoreTransactionalMailingUnsub(models.Model):
    """The core_transactionalmailingaction table stores a row each time a user unsubscribes on a confirmation mailing."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    action = models.ForeignKey(CoreAction, models.DO_NOTHING)
    transactional_mailing_sent = models.ForeignKey(
        CoreTransactionalMailingSent, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "core_transactionalmailingunsub"


class CoreTransactionalMailingClickRaw(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    transactional_mailing_sent = models.ForeignKey(
        CoreTransactionalMailingSent, models.DO_NOTHING
    )
    clickurl = models.ForeignKey(CoreClickUrl, models.DO_NOTHING)
    link_number = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_transactionalmailingclickraw"


class CoreTransactionalMailingOpenRaw(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    transactional_mailing_sent = models.ForeignKey(
        CoreTransactionalMailingSent, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "core_transactionalmailingopenraw"


class CoreUserAgent(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    useragent_string = models.TextField()
    hash = models.CharField(unique=True, max_length=64)
    browser = models.CharField(max_length=255)
    browser_version = models.CharField(max_length=30)
    os = models.CharField(max_length=255)
    os_version = models.CharField(max_length=30)
    device = models.CharField(max_length=255)
    is_mobile = models.IntegerField()
    is_phone = models.IntegerField()
    is_tablet = models.IntegerField()
    is_desktop = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_useragent"


# Texting Tables
class TextingBinding(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    is_default = models.IntegerField()
    title = models.CharField(max_length=64)
    notes = models.CharField(max_length=255)
    enabled = models.IntegerField()

    class Meta:
        managed = False
        db_table = "texting_binding"


class TextingMessage(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    type = models.CharField(max_length=32)
    notes = models.TextField()
    send_type = models.CharField(max_length=32)
    template = models.TextField()
    media_url = models.CharField(max_length=255)
    binding = models.ForeignKey(TextingBinding, models.DO_NOTHING)
    lang = models.ForeignKey(CoreLanguage, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "texting_message"


class TextingAction(models.Model):
    """Action_id and message_id for every action coming from a broadcast or transactional text."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    message = models.ForeignKey(TextingMessage, models.DO_NOTHING)
    action = models.OneToOneField(CoreAction, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_action"


class TextingAdminReplyMessage(models.Model):
    """Pointer to ad hoc text message which was send by an admin to an individual user"""

    message_ptr = models.OneToOneField(
        TextingMessage, models.DO_NOTHING, primary_key=True
    )
    admin_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    change_subscription_status = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "texting_adminreplymessage"


class TextingAfterActionMessage(models.Model):
    """Pointer to text message which may be used as an after-action message. N.b.: Joins to core_pagefollowup via core_pagefollowup.confirmation_text_id"""

    message_ptr = models.OneToOneField(
        TextingMessage, models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "texting_afteractionmessage"


class TextingAllowedTextMessageField(models.Model):
    """Custom field created by your group to display text or activate custom code on a particular page."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    order_index = models.IntegerField()
    display_name = models.CharField(unique=True, max_length=255)
    name = models.CharField(primary_key=True, max_length=128)
    always_show = models.IntegerField()
    required = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    field_type = models.CharField(max_length=32)
    field_default = models.TextField()
    field_choices = models.TextField()
    field_regex = models.TextField()
    field_length = models.IntegerField(blank=True, null=True)
    allow_multiple = models.IntegerField()

    class Meta:
        managed = False
        db_table = "texting_allowedtextmessagefield"


class TextingKeywordResponseMessage(models.Model):
    message_ptr = models.OneToOneField(
        TextingMessage, models.DO_NOTHING, primary_key=True
    )
    subscription_status = models.CharField(max_length=32, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "texting_keywordresponsemessage"


class TextingOriginator(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    gateway = models.CharField(max_length=32)
    address = models.CharField(max_length=32)
    display = models.CharField(max_length=32)
    enabled = models.IntegerField()
    rate_per_minute = models.IntegerField()

    class Meta:
        managed = False
        db_table = "texting_originator"


class TextingBindingOriginators(models.Model):
    binding = models.ForeignKey(TextingBinding, models.DO_NOTHING)
    originator = models.ForeignKey(TextingOriginator, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_binding_originators"
        unique_together = (("binding", "originator"),)


class TextingBlockedRecipient(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    address = models.CharField(unique=True, max_length=64)

    class Meta:
        managed = False
        db_table = "texting_blockedrecipient"


class TextingBlockHistory(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    address = models.CharField(max_length=255)
    message_id = models.IntegerField(blank=True, null=True)
    action_id = models.IntegerField(blank=True, null=True)
    matched_address = models.IntegerField()

    class Meta:
        managed = False
        db_table = "texting_blockhistory"


class TextingBroadcast(models.Model):
    message_ptr = models.OneToOneField(
        TextingMessage, models.DO_NOTHING, primary_key=True
    )
    landing_page = models.ForeignKey(CorePage, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    sent_proofs = models.IntegerField()
    mergefile = models.ForeignKey(
        CoreMergeFile, models.DO_NOTHING, blank=True, null=True
    )
    target_mergefile = models.IntegerField()
    mergequery_report = models.ForeignKey(
        "ReportsQueryReport", models.DO_NOTHING, blank=True, null=True
    )
    target_mergequery = models.IntegerField()
    targeting_version = models.IntegerField(blank=True, null=True)
    targeting_version_saved = models.IntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)
    query_queued_at = models.DateTimeField(blank=True, null=True)
    query_started_at = models.DateTimeField(blank=True, null=True)
    query_completed_at = models.DateTimeField(blank=True, null=True)
    query_previous_runtime = models.IntegerField(blank=True, null=True)
    query_status = models.CharField(max_length=255, blank=True, null=True)
    query_task_id = models.CharField(max_length=255, blank=True, null=True)
    queue_task_id = models.CharField(max_length=255, blank=True, null=True)
    queued_at = models.DateTimeField(blank=True, null=True)
    queued_by = models.ForeignKey(
        AuthUser,
        models.DO_NOTHING,
        related_name="text_broadcast_queued",
        blank=True,
        null=True,
    )
    expected_send_count = models.IntegerField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    requested_proofs = models.IntegerField(blank=True, null=True)
    requested_proof_date = models.DateTimeField(blank=True, null=True)
    submitter = models.ForeignKey(
        AuthUser,
        models.DO_NOTHING,
        related_name="text_broadcast_submitted",
        blank=True,
        null=True,
    )
    target_group_from_landing_page = models.IntegerField()
    respect_recipient_time = models.IntegerField()
    limit = models.IntegerField(blank=True, null=True)
    limit_percent = models.IntegerField(blank=True, null=True)
    sort_by = models.CharField(max_length=32, blank=True, null=True)
    max_per_second = models.FloatField(blank=True, null=True)
    scheduled_for = models.DateTimeField(blank=True, null=True)
    scheduled_by = models.ForeignKey(
        AuthUser,
        models.DO_NOTHING,
        related_name="text_broadcast_scheduled",
        blank=True,
        null=True,
    )
    rebuild_query_at_send = models.IntegerField()

    class Meta:
        managed = False
        db_table = "texting_broadcast"


class TextingBroadcastProofUsers(models.Model):
    broadcast = models.ForeignKey(TextingBroadcast, models.DO_NOTHING)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_broadcast_proof_users"
        unique_together = (("broadcast", "user"),)


class TextingBroadcastReviewers(models.Model):
    broadcast = models.ForeignKey(TextingBroadcast, models.DO_NOTHING)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_broadcast_reviewers"
        unique_together = (("broadcast", "user"),)


class TextingClick(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    message = models.ForeignKey(TextingMessage, models.DO_NOTHING)
    page = models.ForeignKey(CorePage, models.DO_NOTHING, blank=True, null=True)
    click_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "texting_click"


class TextingConfirmationMessage(models.Model):
    message_ptr = models.OneToOneField(
        TextingMessage, models.DO_NOTHING, primary_key=True
    )
    status_trigger = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = "texting_confirmationmessage"


class TextingDeactRun(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    last_deact_notice_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "texting_deactrun"


class TextingSubscriber(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)
    address = models.CharField(max_length=64)
    status = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = "texting_subscriber"
        unique_together = (("user", "address"),)


class TextingMessageSent(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    message = models.ForeignKey(TextingMessage, models.DO_NOTHING)
    subscriber = models.ForeignKey(
        TextingSubscriber, models.DO_NOTHING, blank=True, null=True
    )
    originator = models.ForeignKey(TextingOriginator, models.DO_NOTHING)
    send_type = models.CharField(max_length=32)
    external_id = models.CharField(max_length=255)
    segments = models.IntegerField()
    is_proof = models.IntegerField()
    sent_address = models.CharField(max_length=64, blank=True, null=True)
    sent_in_reply_to = models.ForeignKey(
        "TextingIncomingMessage", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "texting_messagesent"


class TextingDeliveryReceipt(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    gateway = models.CharField(max_length=32)
    for_message = models.ForeignKey(
        TextingMessageSent, models.DO_NOTHING, blank=True, null=True
    )
    payload = models.JSONField()

    class Meta:
        managed = False
        db_table = "texting_deliveryreceipt"


class TextingIncomingMessage(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    status = models.CharField(max_length=16)
    source_address = models.CharField(max_length=24)
    our_address = models.CharField(max_length=24)
    subscriber = models.ForeignKey(
        TextingSubscriber, models.DO_NOTHING, blank=True, null=True
    )
    originator = models.ForeignKey(
        TextingOriginator, models.DO_NOTHING, blank=True, null=True
    )
    prior_send = models.ForeignKey(
        TextingMessageSent, models.DO_NOTHING, blank=True, null=True
    )
    content = models.TextField()

    class Meta:
        managed = False
        db_table = "texting_incomingmessage"


class TextingIncomingSegment(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    status = models.CharField(max_length=16)
    message_at = models.DateTimeField()
    external_uid = models.CharField(max_length=24)
    source_address = models.CharField(max_length=24)
    our_address = models.CharField(max_length=24)
    multipart_uid = models.IntegerField(blank=True, null=True)
    multipart_total = models.IntegerField(blank=True, null=True)
    multipart_part = models.IntegerField(blank=True, null=True)
    content_type = models.CharField(max_length=24)
    content_udh = models.CharField(max_length=24)
    content_data = models.TextField()

    class Meta:
        managed = False
        db_table = "texting_incomingsegment"


class TextingList(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    is_default = models.IntegerField()
    name = models.CharField(unique=True, max_length=255)
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "texting_list"


class TextingMergeQueryParam(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    message = models.ForeignKey(TextingBroadcast, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "texting_mergequeryparam"


class TextingMessageTags(models.Model):
    message = models.ForeignKey(TextingMessage, models.DO_NOTHING)
    tag = models.ForeignKey(CoreTag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_message_tags"
        unique_together = (("message", "tag"),)


class TextingMessageError(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    message = models.ForeignKey(TextingMessage, models.DO_NOTHING)
    queue_task_id = models.CharField(max_length=255)
    traceback = models.TextField()

    class Meta:
        managed = False
        db_table = "texting_messageerror"


class TextingMessageFailed(models.Model):
    created_at = models.DateTimeField()
    message = models.ForeignKey(TextingMessage, models.DO_NOTHING)
    subscriber = models.ForeignKey(TextingSubscriber, models.DO_NOTHING)
    originator = models.ForeignKey(TextingOriginator, models.DO_NOTHING)
    reason = models.TextField()

    class Meta:
        managed = False
        db_table = "texting_messagefailed"


class TextingMessageTargeting(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    message = models.ForeignKey(TextingBroadcast, models.DO_NOTHING)
    exclude = models.IntegerField()
    raw_sql = models.TextField(blank=True, null=True)
    countries = models.TextField(blank=True, null=True)
    states = models.TextField(blank=True, null=True)
    regions = models.TextField(blank=True, null=True)
    counties = models.TextField(blank=True, null=True)
    divisions = models.TextField(blank=True, null=True)
    zips = models.TextField(blank=True, null=True)
    zip_radius = models.IntegerField(blank=True, null=True)
    cds = models.TextField(blank=True, null=True)
    state_senate_districts = models.TextField(blank=True, null=True)
    state_house_districts = models.TextField(blank=True, null=True)
    has_donated = models.IntegerField()
    is_monthly_donor = models.IntegerField()
    campaign_radius = models.IntegerField(blank=True, null=True)
    campaign_samestate_only = models.IntegerField()
    campaign_same_district_only = models.IntegerField()
    campaign_same_county_only = models.IntegerField()
    campaign_first_date = models.CharField(max_length=16)
    campaign_last_date = models.CharField(max_length=16)
    mirror_message_excludes = models.IntegerField()

    class Meta:
        managed = False
        db_table = "texting_messagetargeting"


class TextingMessageTargetingActions(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    page = models.ForeignKey(CorePage, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_actions"
        unique_together = (("messagetargeting", "page"),)


class TextingMessageTargetingBoundaries(models.Model):
    messagetargeting_id = models.IntegerField()
    boundary_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_boundaries"
        unique_together = (("messagetargeting_id", "boundary_id"),)


class TextingMessageTargetingBoundaryGroups(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    boundarygroup = models.ForeignKey(CoreBoundaryGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_boundary_groups"
        unique_together = (("messagetargeting", "boundarygroup"),)


class TextingMessageTargetingCampaigns(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    campaign = models.ForeignKey(EventsCampaign, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_campaigns"
        unique_together = (("messagetargeting", "campaign"),)


class TextingMessageTargetingLanguages(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    language = models.ForeignKey(CoreLanguage, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_languages"
        unique_together = (("messagetargeting", "language"),)


class TextingMessageTargetingLists(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    list = models.ForeignKey("CoreList", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_lists"
        unique_together = (("messagetargeting", "list"),)


class TextingMessageTargetingMailings(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_mailings"
        unique_together = (("messagetargeting", "mailing"),)


class TextingMessageTargetingMessages(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    message = models.ForeignKey(TextingMessage, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_messages"
        unique_together = (("messagetargeting", "message"),)


class TextingMessageTargetingTags(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    tag = models.ForeignKey(CoreTag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_tags"
        unique_together = (("messagetargeting", "tag"),)


class TextingMessageTargetingTargetGroups(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    targetgroup = models.ForeignKey(CoreTargetGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_target_groups"
        unique_together = (("messagetargeting", "targetgroup"),)


class TextingMessageTargetingTextLists(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    list = models.ForeignKey(TextingList, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_text_lists"
        unique_together = (("messagetargeting", "list"),)


class TextingMessageTargetingUserGroups(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    usergroup = models.ForeignKey("CoreUserGroup", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_user_groups"
        unique_together = (("messagetargeting", "usergroup"),)


class TextingMessageTargetingUsers(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    user = models.ForeignKey("CoreUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_users"
        unique_together = (("messagetargeting", "user"),)


class TextingMessageTargetingWasMonthlyDonor(models.Model):
    messagetargeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    recurringdonortargetingoption = models.ForeignKey(
        CoreRecurringDonorTargetingOption, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "texting_messagetargeting_was_monthly_donor"
        unique_together = (("messagetargeting", "recurringdonortargetingoption"),)


class TextingMockGatewayReceived(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    message = models.ForeignKey(TextingMessage, models.DO_NOTHING)
    address = models.CharField(max_length=64)
    originator = models.CharField(max_length=64)
    content = models.TextField()
    delivered = models.IntegerField()

    class Meta:
        managed = False
        db_table = "texting_mockgatewayreceived"


class TextingMockGatewaySent(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    address = models.CharField(max_length=64)
    originator = models.CharField(max_length=64)
    content = models.TextField()
    media_url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "texting_mockgatewaysent"


class TextingReferredAction(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    referring_message = models.ForeignKey(TextingMessage, models.DO_NOTHING)
    action = models.OneToOneField(CoreAction, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_referredaction"


class TextingSavedQueryTimeLog(models.Model):
    message = models.ForeignKey(TextingBroadcast, models.DO_NOTHING)
    sql = models.TextField()
    time = models.FloatField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "texting_savedquerytimelog"


class TextingSavedTextQueryLog(models.Model):
    message = models.ForeignKey(
        TextingBroadcast, models.DO_NOTHING, related_name="log_message"
    )
    process_id = models.IntegerField(blank=True, null=True)
    action = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    targeting_version = models.IntegerField()
    triggered_by = models.ForeignKey(
        TextingBroadcast,
        models.DO_NOTHING,
        related_name="log_triggered",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "texting_savedtextquerylog"


class TextingShortLink(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    link = models.CharField(max_length=4096)
    message = models.ForeignKey(
        TextingMessage, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "texting_shortlink"


class TextingSubscription(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    subscriber = models.ForeignKey(TextingSubscriber, models.DO_NOTHING)
    list = models.ForeignKey(TextingList, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_subscription"
        unique_together = (("subscriber", "list"),)


class TextingSubscriptionChangeType(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True, max_length=24)
    description = models.CharField(max_length=255)
    subscribed = models.IntegerField()

    class Meta:
        managed = False
        db_table = "texting_subscriptionchangetype"


class TextingSubscriptionCountHistory(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    list = models.ForeignKey(TextingList, models.DO_NOTHING, blank=True, null=True)
    date = models.DateField()
    subscribers = models.IntegerField()

    class Meta:
        managed = False
        db_table = "texting_subscriptioncounthistory"


class TextingSubscriptionHistory(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    subscriber = models.ForeignKey(TextingSubscriber, models.DO_NOTHING)
    list = models.ForeignKey(TextingList, models.DO_NOTHING)
    change = models.ForeignKey(TextingSubscriptionChangeType, models.DO_NOTHING)
    action = models.ForeignKey(CoreAction, models.DO_NOTHING, blank=True, null=True)
    incoming_message = models.ForeignKey(
        TextingIncomingMessage, models.DO_NOTHING, blank=True, null=True
    )
    message_sent = models.ForeignKey(
        TextingMessageSent, models.DO_NOTHING, blank=True, null=True
    )
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "texting_subscriptionhistory"


class TextingTargetingActionField(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    targeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    page = models.ForeignKey(CorePage, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    values = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "texting_targetingactionfield"


class TextingTargetingEventField(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    targeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    values = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "texting_targetingeventfield"


class TextingTargetingQueryReport(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    report = models.ForeignKey("ReportsQueryReport", models.DO_NOTHING)
    targeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "texting_targetingqueryreport"


class TextingTargetingQueryReportParam(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    query = models.ForeignKey(TextingTargetingQueryReport, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=4096)

    class Meta:
        managed = False
        db_table = "texting_targetingqueryreportparam"


class TextingTargetingUserField(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    targeting = models.ForeignKey(TextingMessageTargeting, models.DO_NOTHING)
    field = models.ForeignKey("CoreAllowedUserField", models.DO_NOTHING)
    values = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "texting_targetinguserfield"


class TextingTextingSendBroadcastJob(models.Model):
    job_ptr = models.OneToOneField("CoreJob", models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "texting_textingsendbroadcastjob"


class TextingTextMessageCountJob(models.Model):
    job_ptr = models.OneToOneField("CoreJob", models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "texting_textmessagecountjob"


class TextingTextMessageField(models.Model):
    value = models.TextField()
    parent = models.ForeignKey(TextingMessage, models.DO_NOTHING)
    name = models.ForeignKey(
        TextingAllowedTextMessageField, models.DO_NOTHING, db_column="name"
    )

    class Meta:
        managed = False
        db_table = "texting_textmessagefield"


# Import Tables
class CoreUpload(models.Model):
    """Record for each import."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    path = models.CharField(max_length=255)
    submitter = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    format = models.CharField(max_length=10, blank=True, null=True)
    compression = models.CharField(max_length=20, blank=True, null=True)
    autocreate_user_fields = models.IntegerField()
    original_header = models.TextField()
    override_header = models.TextField(blank=True, null=True)
    line_count = models.IntegerField(blank=True, null=True)
    job = models.ForeignKey("CoreJob", models.DO_NOTHING, blank=True, null=True)
    user_fields_only = models.IntegerField(blank=True, null=True)
    user_updater = models.ForeignKey(
        "ReportsUserUpdater", models.DO_NOTHING, blank=True, null=True
    )
    undoable = models.IntegerField()
    undo_table = models.CharField(max_length=255, blank=True, null=True)
    scorepool_job = models.ForeignKey(
        "CoreJob",
        models.DO_NOTHING,
        related_name="upload_scorepool_job",
        blank=True,
        null=True,
    )
    scorepool_score_all = models.IntegerField(blank=True, null=True)
    scorepool_score_new = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_upload"


class CoreUploadError(models.Model):
    """Errors encountered during imports."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    upload = models.ForeignKey(CoreUpload, models.DO_NOTHING)
    worker_pid = models.IntegerField(blank=True, null=True)
    row = models.IntegerField(blank=True, null=True)
    col = models.IntegerField(blank=True, null=True)
    message = models.TextField()
    exception = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    raw_row = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_uploaderror"


class CoreUploadProgress(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    upload = models.ForeignKey(CoreUpload, models.DO_NOTHING)
    worker_pid = models.IntegerField()
    ok = models.IntegerField()
    warnings = models.IntegerField()
    errors = models.IntegerField()
    rate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_uploadprogress"


class CoreUploadWarning(models.Model):
    """Warnings encountered during imports. Warnings indicate possible data problems but they don't cause your import to fail like errors."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    upload = models.ForeignKey(CoreUpload, models.DO_NOTHING)
    worker_pid = models.IntegerField(blank=True, null=True)
    row = models.IntegerField(blank=True, null=True)
    col = models.IntegerField(blank=True, null=True)
    message = models.TextField()
    exception = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    raw_row = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_uploadwarning"


# User Tables
class CoreUser(models.Model):
    """User contact info, user_id, and source of the first action the user took."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255)
    prefix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    subscription_status = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    lang = models.ForeignKey(CoreLanguage, models.DO_NOTHING, blank=True, null=True)
    rand_id = models.IntegerField()
    email_domain = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_user"


class CoreAllowedUserField(models.Model):
    """Field created by your group to capture user-specific data."""

    name = models.CharField(
        primary_key=True, max_length=255, db_collation="utf8mb3_general_ci"
    )
    hidden = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    always_show = models.IntegerField()
    display_name = models.CharField(unique=True, max_length=255)
    order_index = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    field_default = models.TextField()
    field_choices = models.TextField()
    field_regex = models.TextField()
    field_type = models.CharField(max_length=32, db_collation="utf8mb3_general_ci")
    field_length = models.IntegerField(blank=True, null=True)
    required = models.IntegerField()
    allow_multiple = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_alloweduserfield"


class CoreLocation(models.Model):
    """Geography info for each user."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.OneToOneField(CoreUser, models.DO_NOTHING, primary_key=True)
    us_district = models.CharField(max_length=5)
    us_state_senate = models.CharField(max_length=6)
    us_state_district = models.CharField(max_length=6)
    us_county = models.CharField(max_length=255)
    loc_code = models.CharField(max_length=30, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    region_code = models.CharField(max_length=20, blank=True, null=True)
    lat_lon_precision = models.CharField(max_length=32, blank=True, null=True)
    timezone = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_location"


class CorePhone(models.Model):
    """All phone numbers associated with a given user."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    type = models.CharField(max_length=25)
    phone = models.CharField(max_length=25)
    source = models.CharField(max_length=25)
    normalized_phone = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = "core_phone"
        unique_together = (("user", "type", "source"),)


class CoreUserField(models.Model):
    """User field values."""

    id = models.BigAutoField(primary_key=True)
    parent_id = models.IntegerField()
    name = models.ForeignKey(CoreAllowedUserField, models.DO_NOTHING, db_column="name")
    value = models.TextField()
    action = models.ForeignKey(CoreAction, models.DO_NOTHING, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_userfield"


class CoreUserGroup(models.Model):
    """Groups that users can be added to. Similar to tags, except users can be manually added to and removed from groups."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_usergroup"


class CoreUserGroups(models.Model):
    """Record of which users belong to which groups."""

    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    usergroup = models.ForeignKey(CoreUserGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_user_groups"
        unique_together = (("user", "usergroup"),)


class CoreUserMerge(models.Model):
    """Record of users merged."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    primary = models.ForeignKey(CoreUser, models.DO_NOTHING)
    status = models.CharField(max_length=255)
    parent = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)
    sms_primary = models.ForeignKey(
        CoreUser, models.DO_NOTHING, related_name="merge_sms", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "core_usermerge"


class CoreUserMergeUsers(models.Model):
    """Secondary user records merged into primary user. Primary shown in core_usermerge."""

    usermerge = models.ForeignKey(CoreUserMerge, models.DO_NOTHING)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_usermerge_users"
        unique_together = (("usermerge", "user"),)


class CoreUserStaffNote(models.Model):
    """Staff notes on users."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    staff = models.ForeignKey(AuthUser, models.DO_NOTHING)
    note = models.TextField()

    class Meta:
        managed = False
        db_table = "core_userstaffnote"


class CoreUserDivision(models.Model):
    """Match user to international geopolitical divisions."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    division_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_userdivision"
        unique_together = (("user", "division_id"),)


class CoreUserPageTags(models.Model):
    """De-normalized record of user tags. Updated every 10 minutes."""

    user_id = models.IntegerField(primary_key=True)
    tag_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_user_page_tags"
        unique_together = (("user_id", "tag_id"),)


class CoreReengagementLog(models.Model):
    """Daily counts for users engaged and unengaged per the most recently run count, added to the re-engagement list, removed from the re-engagement list, and unsubscribed through list migration."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    dry_run = models.IntegerField()
    engaged = models.IntegerField()
    unengaged = models.IntegerField()
    added = models.IntegerField()
    removed = models.IntegerField()
    unsubscribed = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_reengagementlog"


class OneClickStoredUser(models.Model):
    """Users that are enrolled in the shared FastAction pool."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    fastaction_id = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = "oneclick_storeduser"
        unique_together = (("user", "fastaction_id"),)


class OneClickUse(models.Model):
    """Use of a oneclick donation link in a mailing."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "oneclick_use"


# Subscription Tables
class CoreList(models.Model):
    """Name and id of mailing lists."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    notes = models.CharField(max_length=255, blank=True, null=True)
    hidden = models.IntegerField()
    is_default = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_list"


class CoreSubscription(models.Model):
    """List membership for each subscribed users."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    list = models.ForeignKey(CoreList, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_subscription"
        unique_together = (("user", "list"),)


class CoreSubscriptionChangeType(models.Model):
    """Descriptions of each of the types of changes that are possible to a user's subscription to a particular list."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    subscribed = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_subscriptionchangetype"


class CoreSubscriptionCountHistory(models.Model):
    """Daily subscription counts for each list, and overall."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    list = models.ForeignKey(CoreList, models.DO_NOTHING, blank=True, null=True)
    date = models.DateField()
    subscribers = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_subscriptioncounthistory"


class CoreSubscriptionHistory(models.Model):
    """Changes in subscription status for each user w/ id that ties to changetype table."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    list = models.ForeignKey(CoreList, models.DO_NOTHING)
    change = models.ForeignKey(CoreSubscriptionChangeType, models.DO_NOTHING)
    action = models.ForeignKey(CoreAction, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_subscriptionhistory"


# Job Table
class CoreJob(models.Model):
    """Table with information about back end processing jobs in ActionKit (like uploads or reports)."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    job_type = models.CharField(max_length=255)
    priority = models.IntegerField(blank=True, null=True)
    parameters = models.TextField(blank=True, null=True)
    result_data = models.TextField(blank=True, null=True)
    submitter = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    server = models.CharField(max_length=255, blank=True, null=True)
    pid = models.IntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)
    goal = models.IntegerField(blank=True, null=True)
    estimated_finish_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    django_version = models.CharField(max_length=255, blank=True, null=True)
    polled_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_job"


# CMS Tables
class CmsTemplateset(models.Model):
    """Name and description of a set of templates. Each set has the same templates."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    lang = models.ForeignKey(CoreLanguage, models.DO_NOTHING, blank=True, null=True)
    editable = models.IntegerField()
    hidden = models.IntegerField()
    is_default = models.IntegerField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_templateset"


class CmsAllowedTemplatesetField(models.Model):
    """Allowed templateset fields."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    order_index = models.IntegerField()
    display_name = models.CharField(unique=True, max_length=255)
    name = models.CharField(
        primary_key=True, max_length=255, db_collation="utf8mb3_general_ci"
    )
    always_show = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    field_default = models.TextField()
    field_choices = models.TextField()
    field_regex = models.TextField()
    field_type = models.CharField(max_length=32, db_collation="utf8mb3_general_ci")
    field_length = models.IntegerField(blank=True, null=True)
    required = models.IntegerField()
    allow_multiple = models.IntegerField()

    class Meta:
        managed = False
        db_table = "cms_allowedtemplatesetfield"


class CmsCallForm(models.Model):
    """Call page content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    introduction_text = models.TextField()
    script_text = models.TextField()
    survey_question_text = models.TextField()
    client_hosted = models.IntegerField(blank=True, null=True)
    client_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_call_form"


class CmsCampaignVolunteerForm(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    client_hosted = models.IntegerField()
    client_url = models.CharField(max_length=255)
    ground_rules = models.TextField()
    volunteer_text = models.TextField()

    class Meta:
        managed = False
        db_table = "cms_campaign_volunteer_form"


class CmsLteForm(models.Model):
    """LTE page content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    client_hosted = models.IntegerField()
    client_url = models.CharField(max_length=255)
    introduction_text = models.TextField()
    talking_points = models.TextField()
    writing_tips = models.TextField()

    class Meta:
        managed = False
        db_table = "cms_lte_form"


class CmsCannedLetter(models.Model):
    """Sample letters displayed on LTE forms."""

    lte_form = models.ForeignKey(CmsLteForm, models.DO_NOTHING)
    subject = models.CharField(max_length=80)
    letter_text = models.TextField()

    class Meta:
        managed = False
        db_table = "cms_cannedletter"


class CmsDonationForm(models.Model):
    """Donation page content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    ask_text = models.TextField()
    is_recurring = models.IntegerField()
    show_other_amount = models.IntegerField()
    amount_order = models.CharField(max_length=255)
    client_hosted = models.IntegerField(blank=True, null=True)
    client_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_donation_form"


class CmsDonationAmount(models.Model):
    """Donations also have a subsidiary table showing suggested donation amounts to be displayed on a donation page to the end user."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    amount = models.CharField(max_length=20)
    donation_form = models.ForeignKey(CmsDonationForm, models.DO_NOTHING)
    is_default = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_donationamount"


class CmsEventCreateForm(models.Model):
    """Host event creation page content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    ground_rules = models.TextField()
    host_requirements = models.TextField()
    host_text = models.TextField()
    custom_field_html = models.TextField()
    tools_text = models.TextField()
    tools_sidebar = models.TextField()
    client_hosted = models.IntegerField(blank=True, null=True)
    client_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_event_create_form"


class CmsEventModerateForm(models.Model):
    """Volunteer moderator form for reviewing events, flagging issues, emailing hosts, etc."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    client_hosted = models.IntegerField()
    client_url = models.CharField(max_length=255)
    custom_field_html = models.TextField()
    tools_text = models.TextField()
    tools_sidebar = models.TextField()
    host_tools_sidebar = models.TextField()
    search_page_text = models.TextField()

    class Meta:
        managed = False
        db_table = "cms_event_moderate_form"


class CmsEventSignupForm(models.Model):
    """Attendee event sign up page content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    ground_rules = models.TextField()
    search_page_text = models.TextField()
    signup_text = models.TextField()
    custom_field_html = models.TextField()
    tools_text = models.TextField()
    tools_sidebar = models.TextField()
    client_hosted = models.IntegerField(blank=True, null=True)
    client_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_event_signup_form"


class CmsGithubRepository(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    owner = models.CharField(max_length=255)
    repos = models.CharField(max_length=255)
    private = models.IntegerField()
    public_key = models.TextField(blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    webhook = models.CharField(max_length=255, blank=True, null=True)
    deploy_key = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_githubrepository"
        unique_together = (("owner", "repos"),)


class CmsGithubConnection(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    templateset = models.OneToOneField(CmsTemplateset, models.DO_NOTHING)
    repository = models.ForeignKey(CmsGithubRepository, models.DO_NOTHING)
    path = models.CharField(max_length=255)
    live_branch = models.CharField(max_length=255)
    preview_branch = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "cms_githubconnection"


class CmsGithubEvent(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    body = models.TextField()
    repository = models.ForeignKey(
        CmsGithubRepository, models.DO_NOTHING, blank=True, null=True
    )
    processed_by = models.ForeignKey(CoreJob, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_githubevent"


class CmsGithubWebhookSecret(models.Model):
    secret = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "cms_githubwebhooksecret"


class CmsLetterForm(models.Model):
    """Letter page content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    statement_leadin = models.TextField()
    letter_text = models.TextField()
    about_text = models.TextField()
    client_hosted = models.IntegerField(blank=True, null=True)
    client_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_letter_form"


class CmsPetitionForm(models.Model):
    """Petition content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    statement_leadin = models.TextField()
    statement_text = models.TextField()
    about_text = models.TextField()
    client_hosted = models.IntegerField(blank=True, null=True)
    client_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_petition_form"


class CmsRecurringDonationCancelForm(models.Model):
    """Recurring donation cancellation page content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    please_stay_text = models.TextField()
    client_hosted = models.IntegerField(blank=True, null=True)
    client_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_recurringdonationcancel_form"


class CmsRecurringDonationUpdateForm(models.Model):
    """Recurring donation update page content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    update_card_text = models.TextField()
    client_hosted = models.IntegerField(blank=True, null=True)
    client_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_recurringdonationupdate_form"


class CmsSignupForm(models.Model):
    """Sign up page content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    introduction_text = models.TextField()
    client_hosted = models.IntegerField(blank=True, null=True)
    client_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_signup_form"


class CmsSurveyForm(models.Model):
    """Survey page content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    introduction_text = models.TextField()
    client_hosted = models.IntegerField(blank=True, null=True)
    client_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_survey_form"


class CmsSurveyQuestion(models.Model):
    """Surveys also have a subsidiary table for the survey question html."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    question_label = models.TextField()
    question_html = models.TextField()
    survey_form = models.ForeignKey(CmsSurveyForm, models.DO_NOTHING)
    ordering = models.IntegerField(blank=True, null=True)
    field_type = models.CharField(max_length=16, blank=True, null=True)
    field_name = models.CharField(max_length=255, blank=True, null=True)
    alternatives = models.TextField(blank=True, null=True)
    options_json = models.TextField(blank=True, null=True)
    is_required = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_survey_question"


class CmsTemplate(models.Model):
    """HTML for each template. A template sets the appearance for a page type (like petition) and related items (like list of states)."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    filename = models.CharField(max_length=255)
    code = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    code_hash = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = "cms_template"
        unique_together = (("templateset", "filename"),)


class CmsTemplateCode(models.Model):
    """Stored text of old and current versions of templates for history."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    code_hash = models.CharField(max_length=64)
    code = models.TextField()

    class Meta:
        managed = False
        db_table = "cms_templatecode"


class CmsTemplateHistory(models.Model):
    """Stores old versions of templates."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    filename = models.CharField(max_length=255)
    code_hash = models.CharField(max_length=64)
    user_name = models.CharField(max_length=64, blank=True, null=True)
    edit_type = models.CharField(max_length=64, blank=True, null=True)
    github_sha = models.CharField(max_length=255, blank=True, null=True)
    github_message = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_templatehistory"


class CmsTemplatesetField(models.Model):
    """Templateset field values."""

    parent = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    name = models.ForeignKey(
        CmsAllowedTemplatesetField, models.DO_NOTHING, db_column="name"
    )
    value = models.TextField()

    class Meta:
        managed = False
        db_table = "cms_templatesetfield"


class CmsUnsubscribeForm(models.Model):
    """Unsubscribe page content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    introduction_text = models.TextField()
    survey_question_text = models.TextField()
    client_hosted = models.IntegerField(blank=True, null=True)
    client_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_unsubscribe_form"


class CmsUploadedFile(models.Model):
    """Images, etc. for use in pages."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    bucket = models.CharField(max_length=255)
    directory = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    url = models.CharField(unique=True, max_length=255)
    etag = models.CharField(max_length=255)
    size = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cms_uploadedfile"


class CmsUserFormField(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    form_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    form_id = models.PositiveIntegerField()
    type = models.CharField(max_length=8)
    label = models.TextField()
    field_name = models.CharField(max_length=96)
    input = models.CharField(max_length=16)
    alternatives = models.TextField()
    html = models.TextField()
    status = models.CharField(max_length=8)
    ordering = models.IntegerField()
    options_json = models.TextField()

    class Meta:
        managed = False
        db_table = "cms_user_form_field"


class CmsWhipcountForm(models.Model):
    """Whipcount page content."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    thank_you_text = models.TextField()
    templateset = models.ForeignKey(CmsTemplateset, models.DO_NOTHING)
    page = models.OneToOneField(CorePage, models.DO_NOTHING)
    client_hosted = models.IntegerField()
    client_url = models.CharField(max_length=255)
    introduction_text = models.TextField()
    script_text = models.TextField()
    survey_question_text = models.TextField()
    results_source = models.CharField(max_length=255)
    minimum_response_agreement = models.DecimalField(max_digits=3, decimal_places=2)
    minimum_calls = models.IntegerField()

    class Meta:
        managed = False
        db_table = "cms_whipcount_form"


class CmsWhipcountResponseOverride(models.Model):
    """Holds the admin configuration for overrides for target stances on a whipcount page."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    whipcount_form = models.ForeignKey(CmsWhipcountForm, models.DO_NOTHING)
    target = models.ForeignKey(CoreTarget, models.DO_NOTHING)
    stance = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "cms_whipcountresponseoverride"
        unique_together = (("whipcount_form", "target", "stance"),)


# Page Testing and Statistics Tables
class LabTest(models.Model):
    """An A/B test containing two or more variations, which override selected attributes of the page, like its title or sharing text."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    scope = models.CharField(max_length=12)
    allocation = models.CharField(max_length=32)
    optimize_for = models.CharField(max_length=32, blank=True, null=True)
    change_page_title = models.IntegerField()
    change_intro_text = models.IntegerField()
    change_thanks_text = models.IntegerField()
    change_templateset = models.IntegerField()
    change_custom_fields = models.IntegerField()
    change_followup_url = models.IntegerField()
    change_email_enabled = models.IntegerField()
    change_email_subject = models.IntegerField()
    change_email_body = models.IntegerField()
    change_taf_enabled = models.IntegerField()
    change_taf_subject = models.IntegerField()
    change_taf_body = models.IntegerField()
    change_share_title = models.IntegerField()
    change_share_description = models.IntegerField()
    change_share_image = models.IntegerField()
    change_twitter_message = models.IntegerField()
    change_recognize = models.IntegerField()
    change_statement_text = models.IntegerField()
    change_survey_text = models.IntegerField()
    change_leadin_text = models.IntegerField()
    change_donation_amounts = models.IntegerField()
    change_donation_default = models.IntegerField()
    change_donation_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = "lab_test"


class LabVariation(models.Model):
    """Variations override selected attributes of page in a test, like its title or sharing text."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    test = models.ForeignKey(LabTest, models.DO_NOTHING)
    letter = models.CharField(max_length=2)
    weight = models.FloatField()
    disabled = models.IntegerField()
    page_title = models.CharField(max_length=255)
    intro_text = models.TextField()
    thanks_text = models.TextField()
    templateset = models.ForeignKey(
        CmsTemplateset, models.DO_NOTHING, blank=True, null=True
    )
    followup_url = models.CharField(max_length=255)
    email_enabled = models.CharField(max_length=1)
    email_subject = models.CharField(max_length=255)
    email_body = models.TextField()
    taf_enabled = models.CharField(max_length=1)
    taf_subject = models.CharField(max_length=255)
    taf_body = models.TextField()
    share_title = models.CharField(max_length=255)
    share_description = models.TextField()
    share_image = models.CharField(max_length=255)
    twitter_message = models.CharField(max_length=280, blank=True, null=True)
    recognize = models.CharField(max_length=6)
    statement_text = models.TextField()
    survey_text = models.TextField()
    leadin_text = models.TextField()
    donation_amounts = models.CharField(max_length=255)
    donation_default = models.CharField(max_length=10)
    donation_order = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "lab_variation"


class LabTrial(models.Model):
    """A period during which a test was active."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    test = models.ForeignKey(LabTest, models.DO_NOTHING)
    page = models.ForeignKey(CorePage, models.DO_NOTHING, blank=True, null=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "lab_trial"


class LabEnrollment(models.Model):
    """When a test is active, users who visit a page are “enrolled” with one variation or another, and see that version of the page. Enrollments are sticky between requests, so if a user reloads a page, or clicks away and then returns, they’ll see the same variation again."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    test = models.ForeignKey(LabTest, models.DO_NOTHING)
    variation = models.ForeignKey(LabVariation, models.DO_NOTHING)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING, blank=True, null=True)
    session_key = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "lab_enrollment"


class LabEnrolledAction(models.Model):
    """Records actions taken by users that have been enrolled in a test."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    action = models.ForeignKey(CoreAction, models.DO_NOTHING)
    enrollment = models.ForeignKey(LabEnrollment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "lab_enrolledaction"


class LabEnrolledShare(models.Model):
    """Records a row each time a user enrolled in a test clicks a tracking-enable share button to post a link to a social network."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    share = models.ForeignKey("ShareLink", models.DO_NOTHING)
    enrollment = models.ForeignKey(LabEnrollment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "lab_enrolledshare"


class LabView(models.Model):
    """The lab_view table stores a row for each view of a page that is involved in a test."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    filename = models.CharField(max_length=255)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING, blank=True, null=True)
    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING, blank=True, null=True)
    share = models.ForeignKey("ShareLink", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "lab_view"


class LabEnrolledView(models.Model):
    """Extending lab_view, the lab_enrolledview table records a row for each page view made by a user enrolled in a test."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    view = models.ForeignKey(LabView, models.DO_NOTHING)
    enrollment = models.ForeignKey(LabEnrollment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "lab_enrolledview"


class LabTestPages(models.Model):
    """Pages that have been assigned to a test."""

    test = models.ForeignKey(LabTest, models.DO_NOTHING)
    page = models.ForeignKey(CorePage, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "lab_test_pages"
        unique_together = (("test", "page"),)


class LabTag(models.Model):
    """Categories that can be associated with a test."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = "lab_tag"


class LabTestTags(models.Model):
    """Categories that have been associated with a test."""

    test = models.ForeignKey(LabTest, models.DO_NOTHING)
    tag = models.ForeignKey(LabTag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "lab_test_tags"
        unique_together = (("test", "tag"),)


# Privacy Tables
class CorePrivacyNotes(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    text = models.TextField()

    class Meta:
        managed = False
        db_table = "core_privacynotes"


class CorePrivacyText(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    text = models.TextField()
    type = models.TextField()
    lang = models.ForeignKey(CoreLanguage, models.DO_NOTHING, blank=True, null=True)
    hash = models.CharField(unique=True, max_length=64)
    accepted = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_privacytext"


class CorePrivacyRecord(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    version = models.ForeignKey(CorePrivacyText, models.DO_NOTHING)
    status = models.CharField(max_length=32)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    action = models.ForeignKey(CoreAction, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_privacyrecord"


class EraserLog(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.OneToOneField(CoreUser, models.DO_NOTHING, primary_key=True)
    hashed_email = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "eraser_eraserlog"


# Reports Tables
class ReportsReport(models.Model):
    """Name and basic info about all reports (query or dashboard)."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    short_name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    run_every = models.CharField(max_length=255)
    to_emails = models.CharField(max_length=4000, blank=True, null=True)
    hidden = models.IntegerField()
    help_text = models.TextField()
    send_if_no_rows = models.IntegerField()
    run_day = models.IntegerField(blank=True, null=True)
    run_weekday = models.IntegerField(blank=True, null=True)
    run_hour = models.IntegerField(blank=True, null=True)
    editable = models.IntegerField(blank=True, null=True)
    result_notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "reports_report"


class ReportsDashboardReport(models.Model):
    """HTML for multi query (or dashboard) reports."""

    report_ptr = models.OneToOneField(
        ReportsReport, models.DO_NOTHING, primary_key=True
    )
    template = models.TextField()
    minidash = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "reports_dashboardreport"


class ReportsQueryTemplate(models.Model):
    """Layouts for the queries."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    template = models.TextField()
    hidden = models.IntegerField()
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "reports_querytemplate"


class ReportsQueryReport(models.Model):
    """SQL queries."""

    report_ptr = models.OneToOneField(
        ReportsReport, models.DO_NOTHING, primary_key=True
    )
    sql = models.TextField()
    display_as = models.ForeignKey(ReportsQueryTemplate, models.DO_NOTHING)
    email_always_csv = models.IntegerField(blank=True, null=True)
    refresh = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "reports_queryreport"


class ReportsReportCategory(models.Model):
    """All available report categories."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    hidden = models.IntegerField()
    is_internal = models.IntegerField()

    class Meta:
        managed = False
        db_table = "reports_reportcategory"


class ReportsReportCategories(models.Model):
    """Links report to category."""

    report = models.ForeignKey(ReportsReport, models.DO_NOTHING)
    reportcategory = models.ForeignKey(ReportsReportCategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "reports_report_categories"
        unique_together = (("report", "reportcategory"),)


class ReportsUserUpdater(models.Model):
    """Used to update custom user fields automatically."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    report = models.OneToOneField(ReportsReport, models.DO_NOTHING)
    run_every = models.CharField(max_length=255)
    run_day = models.IntegerField()
    run_weekday = models.IntegerField()
    run_hour = models.IntegerField()
    last_run_job = models.ForeignKey(CoreJob, models.DO_NOTHING, blank=True, null=True)
    last_run_datetime = models.DateTimeField(blank=True, null=True)
    last_run_status = models.CharField(max_length=255, blank=True, null=True)
    last_run_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "reports_userupdater"


class ReportsUserUpdaterStaff(models.Model):
    """Used to determine which staff members get notified of user updater runs."""

    userupdater = models.ForeignKey(ReportsUserUpdater, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "reports_userupdater_staff"


class CoreDefaultExcludeQuery(models.Model):
    """Query report that will be excluded by default when a new mailing is created."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    report = models.ForeignKey(ReportsQueryReport, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_defaultexcludequery"


class CoreDefaultExcludeQueryParam(models.Model):
    """Additional parameters provided by staffer when using a query report as an auto excludes query."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    query = models.ForeignKey(CoreDefaultExcludeQuery, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_defaultexcludequeryparam"


class CoreEngagementQueryReport(models.Model):
    """Query report used to identify engaged users for re-engagement processing."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    report = models.ForeignKey(ReportsQueryReport, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_engagementqueryreport"


class CoreEngagementQueryReportParam(models.Model):
    """Additional parameters provided by staffer when using a query report to identify engaged users."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    query = models.ForeignKey(CoreEngagementQueryReport, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_engagementqueryreportparam"


class CoreDatabaseAccount(models.Model):
    """Accounts that have been granted access to the MySQL client analytics database."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    username = models.CharField(unique=True, max_length=32)
    email = models.CharField(max_length=255, blank=True, null=True)
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_databaseaccount"


# Sharing Tables
class ShareLink(models.Model):
    """The share_link table stores a row each time a user clicks a tracking-enabled share button to post a link to a social network."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    type = models.CharField(max_length=2)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING, blank=True, null=True)
    action = models.ForeignKey(CoreAction, models.DO_NOTHING, blank=True, null=True)
    referring_share = models.ForeignKey(
        "self", models.DO_NOTHING, blank=True, null=True
    )
    generation = models.PositiveSmallIntegerField()
    source = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "share_link"


class ShareType(models.Model):
    """Records the names and two-letter type codes associated with various types of sharing, including Facebook, Twitter, and other."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type = models.CharField(max_length=2)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "share_type"


class ShareAction(models.Model):
    """The share_action table stores a row each time a user takes action after clicking on a trackable share link."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    share = models.ForeignKey(ShareLink, models.DO_NOTHING)
    action = models.OneToOneField(CoreAction, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "share_action"


class ShareClick(models.Model):
    """The share_click table stores a row each time a user clicks on a trackable share link."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    share = models.ForeignKey(ShareLink, models.DO_NOTHING)
    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    click_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "share_click"


# Delivery Tables
class CoreBatchDelivery(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    target = models.ForeignKey(CoreTarget, models.DO_NOTHING)
    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    message = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    from_line = models.TextField(blank=True, null=True)
    recent_signatures = models.IntegerField()
    recent_since = models.DateTimeField()
    delivered = models.IntegerField()
    traceback = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_batchdelivery"


class CoreDeliveryError(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    page = models.ForeignKey(CorePage, models.DO_NOTHING)
    target = models.ForeignKey(CoreTarget, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    subject = models.TextField()
    body = models.TextField()
    reason = models.CharField(max_length=255)
    delivery_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_deliveryerror"


class CorePetitionDeliveryFile(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    job = models.ForeignKey(CorePetitionDeliveryJob, models.DO_NOTHING)
    target_count = models.IntegerField()
    signatures = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    filename = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_petitiondeliveryfile"


class CorePetitionDeliveryFileTargets(models.Model):
    petitiondeliveryfile = models.ForeignKey(
        CorePetitionDeliveryFile, models.DO_NOTHING
    )
    target = models.ForeignKey(CoreTarget, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_petitiondeliveryfile_targets"
        unique_together = (("petitiondeliveryfile", "target"),)


class CorePetitionDeliveryFileCollector(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    task_id = models.CharField(max_length=255, blank=True, null=True)
    queued = models.IntegerField()
    completed = models.IntegerField()
    status = models.CharField(max_length=255)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    job = models.ForeignKey(CorePetitionDeliveryJob, models.DO_NOTHING)
    format = models.CharField(max_length=255)
    archive = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_petitiondeliveryfilecollector"


class CorePetitionDeliveryFileDownload(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    file = models.ForeignKey(CorePetitionDeliveryFile, models.DO_NOTHING)
    downloaded_by = models.ForeignKey("CoreTarget", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_petitiondeliveryfiledownload"


class CorePetitionDeliveryJobBuilder(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    job = models.ForeignKey(CorePetitionDeliveryJob, models.DO_NOTHING)
    task_id = models.CharField(max_length=255, blank=True, null=True)
    queued = models.IntegerField()
    completed = models.IntegerField()
    status = models.CharField(max_length=255)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_petitiondeliveryjobbuilder"


# Salesforce Integration Tables
class CoreSalesforceFieldMap(models.Model):
    """User field mappings for your Salesforce integration."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    ak_field = models.CharField(max_length=255)
    sf_field = models.CharField(max_length=255)
    readonly = models.IntegerField()
    direction = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_salesforcefieldmap"


class CoreSalesforceLog(models.Model):
    """Summary of each time the sync runs."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    last_sf_datetime = models.DateTimeField(blank=True, null=True)
    last_ak_user_id = models.IntegerField(blank=True, null=True)
    last_ak_action_id = models.IntegerField(blank=True, null=True)
    created_ak_users = models.IntegerField()
    created_ak_orders = models.IntegerField()
    created_sf_users = models.IntegerField()
    created_sf_opportunities = models.IntegerField()
    updated_ak_users = models.IntegerField()
    updated_sf_users = models.IntegerField()
    failed_ak_users = models.IntegerField()
    failed_sf_users = models.IntegerField()
    status = models.CharField(max_length=20)
    error = models.TextField(blank=True, null=True)
    created_sf_recurring = models.IntegerField()
    last_ak_updated_at = models.DateTimeField(blank=True, null=True)
    last_ak_uf_updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_salesforcelog"


class CoreSalesforceOrderFieldMap(models.Model):
    """Order field mappings for your Salesforce integration."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    ak_field = models.CharField(max_length=255)
    ak_literal = models.CharField(max_length=255)
    sf_field = models.CharField(max_length=255)
    sf_literal = models.CharField(max_length=255)
    readonly = models.IntegerField()
    direction = models.CharField(max_length=255)
    builtin = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_salesforceorderfieldmap"


class CoreSalesforceOrderMap(models.Model):
    """Record of synced donations."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    order = models.ForeignKey(CoreOrder, models.DO_NOTHING)
    salesforce_id = models.CharField(max_length=18)
    origin = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = "core_salesforceordermap"
        unique_together = (("order", "salesforce_id"),)


class CoreSalesforceRecurringOrderFieldMap(models.Model):
    """Recurring order field mappings for your Salesforce integration."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    ak_field = models.CharField(max_length=255)
    ak_literal = models.CharField(max_length=255)
    sf_field = models.CharField(max_length=255)
    sf_literal = models.CharField(max_length=255)
    readonly = models.IntegerField()
    builtin = models.IntegerField()
    direction = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_salesforcerecurringorderfieldmap"


class CoreSalesforceSyncRule(models.Model):
    """Not in use."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    sf_field = models.CharField(max_length=255)
    rule_type = models.CharField(max_length=255)
    operation = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_salesforcesyncrule"


class CoreSalesforceTransactionMap(models.Model):
    """Maps individual payments on recurring orders from core_transaction to the corresponding Salesforce opportunity."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    transaction = models.ForeignKey(CoreTransaction, models.DO_NOTHING)
    salesforce_id = models.CharField(max_length=18)

    class Meta:
        managed = False
        db_table = "core_salesforcetransactionmap"
        unique_together = (("transaction", "salesforce_id"),)


class CoreSalesforceUserFailedSync(models.Model):
    """Record of failed sync attempts for specific users."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    reason = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = "core_salesforceuserfailedsync"


class CoreSalesforceUserMap(models.Model):
    """Record of user to contact mapping and whether the record was newly created in each system."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    salesforce_id = models.CharField(max_length=18)
    match_type = models.CharField(max_length=255)
    created_ak_user = models.IntegerField()
    created_sf_user = models.IntegerField()
    last_sync_at = models.DateTimeField(blank=True, null=True)
    id_match = models.IntegerField(blank=True, null=True)
    email_match = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_salesforceusermap"
        unique_together = (("user", "salesforce_id"),)


class CoreSalesforceAddressUpdatedQueue(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    sent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_salesforceaddressupdatedqueue"


class CoreSalesforceApilLog(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    method = models.CharField(max_length=255)
    params = models.TextField()
    filename = models.CharField(max_length=255)
    line = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_salesforceapilog"


class CoreSalesforceSyncTemplate(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    template = models.TextField()
    sync = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_salesforcesynctemplate"


class CoreHistoricalSalesforceFieldMap(models.Model):
    """This stored previous version of user field mappings. Joins to core_salesforcefieldmap."""

    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    ak_field = models.CharField(max_length=255)
    sf_field = models.CharField(max_length=255)
    readonly = models.IntegerField(blank=True, null=True)
    direction = models.CharField(max_length=255)
    history_id = models.IntegerField()
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_historicalsalesforcefieldmap"


class CoreHistoricalSalesforceOrderFieldMap(models.Model):
    """This stored previous version of order field mappings. Joins to core_salesforceorderfieldmap."""

    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    ak_field = models.CharField(max_length=255)
    ak_literal = models.CharField(max_length=255)
    sf_field = models.CharField(max_length=255)
    sf_literal = models.CharField(max_length=255)
    readonly = models.IntegerField(blank=True, null=True)
    builtin = models.IntegerField(blank=True, null=True)
    direction = models.CharField(max_length=255)
    history_id = models.IntegerField()
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_historicalsalesforceorderfieldmap"


class CoreHistoricalSalesforceRecurringOrderFieldMap(models.Model):
    """This stored previous version of recurring order field mappings. Joins to core_salesforcerecurringorderfieldmap."""

    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    ak_field = models.CharField(max_length=255)
    ak_literal = models.CharField(max_length=255)
    sf_field = models.CharField(max_length=255)
    sf_literal = models.CharField(max_length=255)
    readonly = models.IntegerField(blank=True, null=True)
    builtin = models.IntegerField(blank=True, null=True)
    direction = models.CharField(max_length=255)
    history_id = models.IntegerField()
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_historicalsalesforcerecurringorderfieldmap"


# EveryAction Integration Tables
class CoreEveryActionAccountMap(models.Model):
    """Mapping of ActionKit payment accounts to EveryAction designations."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    account = models.CharField(unique=True, max_length=255)
    designation_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_everyactionaccountmap"


class CoreEveryActionApiLog(models.Model):
    """Log of all EveryAction API calls made"""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    method = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    line = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_everyactionapilog"


class CoreEveryActionBulkMapping(models.Model):
    """Stores mapping data for use with the EveryAction Bulk Upload API"""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=255)
    result_name = models.CharField(max_length=255)
    readonly = models.IntegerField()
    sync = models.CharField(max_length=255)
    hidden = models.IntegerField()
    virtual = models.IntegerField()
    direction = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = "core_everyactionbulkmapping"


class CoreEveryActionBulkMappingField(models.Model):
    """Stores field definitions for bulk mappings, used to construct input for the EveryAction Bulk Upload API."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    mapping = models.ForeignKey(CoreEveryActionBulkMapping, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    readonly = models.IntegerField()
    hidden = models.IntegerField()
    column = models.CharField(max_length=255, blank=True, null=True)
    ak_field = models.CharField(max_length=255, blank=True, null=True)
    fmt = models.CharField(max_length=255, blank=True, null=True)
    static = models.CharField(max_length=255, blank=True, null=True)
    output = models.IntegerField()
    ord = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_everyactionbulkmappingfield"


class CoreEveryActionLog(models.Model):
    """This tables stores a row for every run of the EveryAction sync, recording status info."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    last_ak_user_id = models.IntegerField(blank=True, null=True)
    last_ak_action_id = models.IntegerField(blank=True, null=True)
    last_ak_updated_at = models.DateTimeField(blank=True, null=True)
    created_ea_contacts = models.IntegerField()
    updated_ea_contacts = models.IntegerField()
    failed_ea_contacts = models.IntegerField()
    created_ea_contributions = models.IntegerField()
    updated_ea_contributions = models.IntegerField()
    failed_ea_contributions = models.IntegerField()
    status = models.CharField(max_length=20)
    error = models.TextField(blank=True, null=True)
    last_ak_uf_updated_at = models.DateTimeField(blank=True, null=True)
    created_ak_users = models.IntegerField()
    updated_ak_users = models.IntegerField()
    failed_ak_users = models.IntegerField()
    last_ea_contact_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_everyactionlog"


class CoreEveryActionMergeQuery(models.Model):
    """This table holds data related to merge queries used in the EA sync."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    sync = models.CharField(max_length=255)
    report = models.ForeignKey(
        ReportsQueryReport, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "core_everyactionmergequery"


class CoreEveryActionOrderFailedSync(models.Model):
    """This table holds orders that failed to sync to EA along with error details. This is used to control retry frequency in the sync."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    order = models.ForeignKey(CoreOrder, models.DO_NOTHING)
    reason = models.TextField()

    class Meta:
        managed = False
        db_table = "core_everyactionorderfailedsync"


class CoreEveryActionOrderMap(models.Model):
    """Table mapping ActionKit orders (one-time and recurring) to EveryAction Contributions and Recurring Donations."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    order = models.ForeignKey(CoreOrder, models.DO_NOTHING)
    contribution_id = models.IntegerField()
    origin = models.CharField(max_length=2)
    is_recurring = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_everyactionordermap"
        unique_together = (("order", "contribution_id"),)


class CoreEveryActionRestCallLog(models.Model):
    """Log of calls to the ActionKit REST API EveryAction resources."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    method = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    body = models.TextField()
    result = models.TextField()
    status_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_everyactionrestcalllog"


class CoreEveryActionTransactionFailedSync(models.Model):
    """This table holds recurring payments that failed to sync to EA along with error details. This is used to control retry frequency in the sync."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    transaction = models.ForeignKey(CoreTransaction, models.DO_NOTHING)
    reason = models.TextField()

    class Meta:
        managed = False
        db_table = "core_everyactiontransactionfailedsync"


class CoreEveryActionTransactionMap(models.Model):
    """Table mapping ActionKit recurring payments to EveryAction Contributions."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    transaction = models.ForeignKey(CoreTransaction, models.DO_NOTHING)
    contribution_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_everyactiontransactionmap"
        unique_together = (("transaction", "contribution_id"),)


class CoreEveryActionUserFailedSync(models.Model):
    """This table holds users that failed to sync to EA along with error details. This is used to control retry frequency in the sync."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    reason = models.TextField()

    class Meta:
        managed = False
        db_table = "core_everyactionuserfailedsync"


class CoreEveryActionUserMap(models.Model):
    """Table mapping ActionKit users to EveryAction Contacts."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    van_id = models.IntegerField()
    created_ea_contact = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_everyactionusermap"


# ActBlue Integration Tables
class WebhookNotificationReceived(models.Model):
    """Stores received webhook events. Only contains recent data; older data is regularly deleted. See webhooks_webhooknotificationreceivedlog for historical data."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=255)
    error = models.TextField()
    retries = models.IntegerField()

    class Meta:
        managed = False
        db_table = "webhooks_webhooknotificationreceived"


class WebhookNotificationReceivedLog(models.Model):
    """Like webhooks_webhooknotificationreceived, but also contains historical data and the column actblue_id which can be joined to core_order on import_id."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=255)
    error = models.TextField()
    retries = models.IntegerField()
    actblue_id = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "webhooks_webhooknotificationreceivedlog"


class CoreActBlueTransactionDetail(models.Model):
    """Connects core_transaction and core_order_detail, so we can aggregate multiple ActBlue notifications into a single Transaction without duplicates. This allows us to identify information including amounts donated by candidate on the transaction level."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    transaction = models.ForeignKey(CoreTransaction, models.DO_NOTHING)
    detail = models.ForeignKey(CoreOrderDetail, models.DO_NOTHING)
    sequence = models.IntegerField()
    lineitem_id = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_converted = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    currency = models.CharField(max_length=3, blank=True, null=True)
    candidate = models.ForeignKey(
        CoreCandidate, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "core_actbluetransactiondetail"
        unique_together = (("lineitem_id", "type"),)


# Config/Admin Tables
class CoreAdminEditors(models.Model):
    """Default settings for text editors in your instance."""

    visual_default = models.CharField(max_length=16)
    template_default = models.CharField(max_length=16)
    turn_off_visual = models.IntegerField()
    bee_editor_enabled = models.IntegerField()
    bee_collaborative_editing_enabled = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_admineditors"


class CoreClientSetting(models.Model):
    """CONFIG settings."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    entity = models.CharField(max_length=255)
    attribute = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = "core_clientsetting"
        unique_together = (("entity", "attribute"),)


class CoreDonationConfiguration(models.Model):
    """Donation processing settings for your instance. Set on CONFIG screen."""

    duplicate_window = models.IntegerField(blank=True, null=True)
    send_ip_address = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_donationconfiguration"


class CoreMailingsConfig(models.Model):
    """Settings for your instance for auto-excludes. Set on CONFIG screen."""

    use_auto_excludes = models.IntegerField()
    send_date_default = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_mailingsconfig"


class CoreNotice(models.Model):
    """Announcements created by Staff Users and displayed for all staff in the admin UI."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    title = models.TextField()
    message = models.TextField()
    type = models.CharField(max_length=10)
    url = models.TextField()
    tag = models.CharField(max_length=255)
    expiration = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    creator = models.ForeignKey(
        AuthUser,
        models.DO_NOTHING,
        related_name="notice_creator",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "core_notice"


class CoreNoticeClosed(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    notice = models.ForeignKey(CoreNotice, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_noticeclosed"


class CoreSupportContact(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    contact = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_supportcontact"


class PushEndpoint(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.IntegerField()
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255, db_collation="utf8mb4_unicode_ci")
    triggers = models.JSONField()
    ratelimit = models.IntegerField()
    retries = models.IntegerField()
    handler_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "push_endpoint"


# Summary Tables
class SummaryUser(models.Model):
    """A collection of summary statistics for users, useful for finding active or inactive users. Users with none of the activities monitored here in the past year will not be in this table. These statistics are updated hourly, but changes to older data, e.g. changing the "Include In Reports of Member Actions" setting on a page or modifying timestamps of existing orders via API, won't be picked up immediately."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user_id = models.IntegerField(primary_key=True)
    last_action = models.DateTimeField(blank=True, null=True)
    last_mailing_action = models.DateTimeField(blank=True, null=True)
    last_open = models.DateTimeField(blank=True, null=True)
    last_click = models.DateTimeField(blank=True, null=True)
    last_subscribed = models.DateTimeField(blank=True, null=True)
    last_donation = models.DateTimeField(blank=True, null=True)
    actions_last_30_days = models.SmallIntegerField(blank=True, null=True)
    actions_last_60_days = models.SmallIntegerField(blank=True, null=True)
    actions_last_90_days = models.SmallIntegerField(blank=True, null=True)
    actions_last_180_days = models.SmallIntegerField(blank=True, null=True)
    actions_last_270_days = models.SmallIntegerField(blank=True, null=True)
    actions_last_365_days = models.SmallIntegerField(blank=True, null=True)
    last_mailed = models.DateTimeField(blank=True, null=True)
    last_raw_open = models.DateTimeField(blank=True, null=True)
    mailbox_provider = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "summary_user"


class SummaryMailing(models.Model):
    """A collection of summary statistics for mailings, useful for reviewing mailing performance."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    mailing_id = models.IntegerField(primary_key=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    recipients = models.IntegerField(blank=True, null=True)
    total_opens = models.IntegerField(blank=True, null=True)
    total_raw_opens = models.IntegerField(blank=True, null=True)
    opens = models.IntegerField(blank=True, null=True)
    raw_opens = models.IntegerField(blank=True, null=True)
    total_clicks = models.IntegerField(blank=True, null=True)
    actions = models.IntegerField(blank=True, null=True)
    orders = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_converted = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    unsubscribes = models.IntegerField(blank=True, null=True)
    bounces = models.IntegerField(blank=True, null=True)
    complaints = models.IntegerField(blank=True, null=True)
    total_raw_clicks = models.IntegerField(blank=True, null=True)
    clicks = models.IntegerField(blank=True, null=True)
    raw_clicks = models.IntegerField(blank=True, null=True)
    bounces_all = models.IntegerField()
    total_unsubscribes = models.IntegerField()
    new_users = models.IntegerField()
    delays = models.IntegerField()

    class Meta:
        managed = False
        db_table = "summary_mailing"


class SummaryMailingSubject(models.Model):
    """A collection of summary statistics for mailings, grouped by subject. Subject ID will be 0 in cases where the subject is unknown (forwarded mailings, for example)."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    mailing_id = models.IntegerField()
    subject_id = models.IntegerField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    recipients = models.IntegerField(blank=True, null=True)
    opens = models.IntegerField(blank=True, null=True)
    raw_opens = models.IntegerField(blank=True, null=True)
    total_opens = models.IntegerField(blank=True, null=True)
    total_raw_opens = models.IntegerField(blank=True, null=True)
    clicks = models.IntegerField(blank=True, null=True)
    raw_clicks = models.IntegerField(blank=True, null=True)
    total_clicks = models.IntegerField(blank=True, null=True)
    total_raw_clicks = models.IntegerField(blank=True, null=True)
    actions = models.IntegerField(blank=True, null=True)
    orders = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_converted = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    unsubscribes = models.IntegerField(blank=True, null=True)
    bounces = models.IntegerField(blank=True, null=True)
    complaints = models.IntegerField(blank=True, null=True)
    total_unsubscribes = models.IntegerField()
    new_users = models.IntegerField()
    bounces_all = models.IntegerField()
    delays = models.IntegerField()

    class Meta:
        managed = False
        db_table = "summary_mailingsubject"
        unique_together = (("mailing_id", "subject_id"),)


class SummaryMailingVariation(models.Model):
    """A collection of summary statistics for mailings, grouped by variation when using inline A/B testing."""

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    mailing = models.ForeignKey(CoreMailing, models.DO_NOTHING)
    variation_id = models.IntegerField(blank=True, null=True)
    letter = models.CharField(max_length=2, blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    recipients = models.IntegerField()
    opens = models.IntegerField()
    raw_opens = models.IntegerField()
    total_opens = models.IntegerField()
    total_raw_opens = models.IntegerField()
    clicks = models.IntegerField()
    raw_clicks = models.IntegerField()
    total_clicks = models.IntegerField()
    total_raw_clicks = models.IntegerField()
    actions = models.IntegerField()
    orders = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_converted = models.DecimalField(max_digits=10, decimal_places=2)
    unsubscribes = models.IntegerField()
    bounces = models.IntegerField()
    complaints = models.IntegerField()
    total_unsubscribes = models.IntegerField()
    new_users = models.IntegerField()
    bounces_all = models.IntegerField()
    delays = models.IntegerField()

    class Meta:
        managed = False
        db_table = "summary_mailingvariation"
        unique_together = (("mailing", "variation_id"),)


# Internal Use Only Tables
## These tables are not for use by client.
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_groups"
        unique_together = (("user", "group"),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_user_permissions"
        unique_together = (("user", "permission"),)


class AxesAccessAttempt(models.Model):
    user_agent = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=39, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    http_accept = models.CharField(max_length=1025)
    path_info = models.CharField(max_length=255)
    attempt_time = models.DateTimeField()
    get_data = models.TextField()
    post_data = models.TextField()
    failures_since_start = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = "axes_accessattempt"


class Cache(models.Model):
    cache_key = models.CharField(primary_key=True, max_length=255)
    value = models.TextField()
    expires = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "cache"


class CoreAdminLocation(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    admin = models.ForeignKey(AuthUser, models.DO_NOTHING)
    ip_address = models.CharField(max_length=15, blank=True, null=True)
    user_agent = models.ForeignKey(
        CoreUserAgent, models.DO_NOTHING, blank=True, null=True
    )
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_adminlocation"


class CoreAdminNoticeLog(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(max_length=255)
    notice_type = models.CharField(max_length=255, blank=True, null=True)
    object_type = models.CharField(max_length=40)
    object_id = models.IntegerField()
    subject = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_adminnoticelog"


class CoreAdminPrefs(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    ordering = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_adminprefs"
        unique_together = (("user", "content_type"),)


class CoreBlockedEmail(models.Model):
    mailing_id = models.IntegerField()
    user_id = models.IntegerField()
    code = models.SmallIntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_blocked_email"
        unique_together = (("mailing_id", "user_id"),)


class CoreBounceState(models.Model):
    bounce_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "core_bounce_state"


class CoreDonationAttemptLog(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    accept = models.CharField(max_length=255)
    accept_encoding = models.CharField(max_length=255)
    accept_language = models.CharField(max_length=255)
    accept_charset = models.CharField(max_length=255)
    referrer = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    user_agent_odd = models.IntegerField()
    user_agent_hash = models.CharField(max_length=255)
    has_session = models.IntegerField()
    args = models.TextField()
    maxmind_score = models.FloatField()
    maxmind_response = models.TextField()
    was_filtered = models.IntegerField()
    filter_name = models.CharField(max_length=30, blank=True, null=True)
    order = models.ForeignKey(CoreOrder, models.DO_NOTHING, blank=True, null=True)
    action = models.ForeignKey(
        CoreDonationAction, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "core_donationattemptlog"


class CoreFacebookApp(models.Model):
    app_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_facebookapp"


class CoreFaxAccount(models.Model):
    email = models.CharField(max_length=255)
    from_email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_faxaccount"


class CoreGoogleAnalytics(models.Model):
    key = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_googleanalytics"


class CoreHostingPlatform(models.Model):
    name = models.CharField(unique=True, max_length=255)
    after_basics_redirect_url = models.CharField(max_length=255)
    after_basics_redirect_name = models.CharField(max_length=255)
    end_redirect_url = models.CharField(max_length=255)
    end_redirect_name = models.CharField(max_length=255)
    after_action_redirect_url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_hostingplatform"


class CoreJobState(models.Model):
    job = models.CharField(primary_key=True, max_length=255)
    attribute = models.CharField(max_length=255)
    value = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_job_state"
        unique_together = (("job", "attribute"),)


class CoreJobcron(models.Model):
    created_at = models.DateTimeField()
    interval = models.CharField(primary_key=True, max_length=255)
    span = models.PositiveIntegerField()
    server = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_jobcron"
        unique_together = (("interval", "span"),)


class CoreJobError(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    job = models.ForeignKey(CoreJob, models.DO_NOTHING)
    message = models.TextField()
    exception = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_joberror"


class CoreJobSignal(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    job = models.ForeignKey(CoreJob, models.DO_NOTHING)
    signal = models.CharField(max_length=20, blank=True, null=True)
    recieved = models.IntegerField()
    recieved_at = models.DateTimeField(blank=True, null=True)
    submitter = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_jobsignal"


class CoreJobStatusLog(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    job = models.ForeignKey(CoreJob, models.DO_NOTHING)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = "core_jobstatuslog"


class CorePageFollowupPushes(models.Model):
    pagefollowup = models.ForeignKey(CorePageFollowup, models.DO_NOTHING)
    endpoint = models.ForeignKey(PushEndpoint, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_pagefollowup_pushes"
        unique_together = (("pagefollowup", "endpoint"),)


class CorePreviousPageTags(models.Model):
    page_id = models.IntegerField(primary_key=True)
    tag_id = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_previous_page_tags"
        unique_together = (("page_id", "tag_id"),)


class CoreRedirectPage(models.Model):
    page_ptr = models.OneToOneField(CorePage, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_redirectpage"


class CoreS3Connection(models.Model):
    access_key = models.CharField(max_length=255)
    bucket = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_s3connection"


class CoreSavedQueryLog(models.Model):
    created_at = models.DateTimeField()
    mailing_id = models.IntegerField()
    action = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    triggered_by_id = models.IntegerField(blank=True, null=True)
    process_id = models.IntegerField(blank=True, null=True)
    targeting_version = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_savedquerylog"


class CoreSavedQueryTimeLog(models.Model):
    mailing_id = models.IntegerField()
    sql = models.TextField()
    time = models.FloatField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_savedquerytimelog"


class CoreSession(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    action = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)
    session_key = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_session"


class CoreSubscriptionHistorySyncedToSendgrid(models.Model):
    subscriptionhistory_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "core_subscriptionhistory_synced_to_sendgrid"


class CoreTargetContact(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    target = models.ForeignKey(CoreTarget, models.DO_NOTHING, blank=True, null=True)
    email = models.CharField(max_length=255)
    is_current = models.IntegerField()
    prefix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    is_mailable = models.IntegerField()
    email_version_hash = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_targetcontact"


class CoreTellAFriendAction(models.Model):
    action_ptr = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "core_tellafriendaction"


class CoreTimezonePreference(models.Model):
    tz_name = models.CharField(max_length=64)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_timezonepreference"


class CoreTodayTimezone(models.Model):
    tz_name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = "core_todaytimezone"


class CoreTransactionalMailingTags(models.Model):
    transactionalmailing = models.ForeignKey(
        CoreTransactionalMailing, models.DO_NOTHING
    )
    tag = models.ForeignKey(CoreTag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_transactionalmailing_tags"
        unique_together = (("transactionalmailing", "tag"),)


class CoreUnsubEmail(models.Model):
    user_id = models.IntegerField()
    mailing_id = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField()
    action_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_unsub_email"
        unique_together = (
            ("user_id", "action_id"),
            ("user_id", "mailing_id"),
        )


class CoreUnsubEmailState(models.Model):
    unsub_email_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "core_unsub_email_state"


class CoreUserGeoField(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_usergeofield"


class CoreUsermailingArchiveModel(models.Model):
    id = models.IntegerField(primary_key=True)
    mailing_id = models.IntegerField()
    user_id = models.IntegerField()
    subject_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_usermailing_archive_model"


class CoreUserMailingArchiveState(models.Model):
    mailing_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "core_usermailing_archive_state"


class CoreUserOriginal(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.OneToOneField(CoreUser, models.DO_NOTHING, primary_key=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    address1_updated_at = models.DateTimeField(blank=True, null=True)
    address2_updated_at = models.DateTimeField(blank=True, null=True)
    city_updated_at = models.DateTimeField(blank=True, null=True)
    state_updated_at = models.DateTimeField(blank=True, null=True)
    zip_updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_useroriginal"


class CoreGeocodeQueue(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_geocodequeue"


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoAgentTrustAgentSettings(models.Model):
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)
    trust_days = models.FloatField(blank=True, null=True)
    inactivity_days = models.FloatField(blank=True, null=True)
    serial = models.IntegerField()

    class Meta:
        managed = False
        db_table = "django_agent_trust_agentsettings"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class DjangoSite(models.Model):
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "django_site"


class LabMetric(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "lab_metric"


class LabPageType(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "lab_pagetype"


class LabTestCustomFields(models.Model):
    test = models.ForeignKey(LabTest, models.DO_NOTHING)
    allowedpagefield = models.ForeignKey(CoreAllowedPageField, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "lab_test_custom_fields"
        unique_together = (("test", "allowedpagefield"),)


class LabTestPageTypes(models.Model):
    test = models.ForeignKey(LabTest, models.DO_NOTHING)
    pagetype = models.ForeignKey(LabPageType, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "lab_test_page_types"
        unique_together = (("test", "pagetype"),)


class RenamedCoreTransactionsCorePayment(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    order = models.ForeignKey(CoreOrder, models.DO_NOTHING)
    account = models.CharField(max_length=255)
    test_mode = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    success = models.IntegerField()
    trans_id = models.CharField(max_length=255, blank=True, null=True)
    failure_description = models.CharField(max_length=255)
    failure_code = models.IntegerField(blank=True, null=True)
    failure_message = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "renamed_core_transactions_core_payment"


class ReportsCachedQueryResult(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    report = models.ForeignKey(ReportsQueryReport, models.DO_NOTHING)
    sql = models.TextField()
    params = models.TextField()
    cache_table = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "reports_cachedqueryresult"


class SpamCheckerActionState(models.Model):
    action = models.OneToOneField(CoreAction, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = "spam_checkeractionstate"


class TastypieApiAccess(models.Model):
    identifier = models.CharField(max_length=255)
    url = models.TextField()
    request_method = models.CharField(max_length=10)
    accessed = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = "tastypie_apiaccess"


class TastypieApiKey(models.Model):
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)
    key = models.CharField(max_length=256)
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "tastypie_apikey"


# Not Specified, likely internal also
class RIdTemp(models.Model):
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "R_id_temp"


class RIdTemp2(models.Model):
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "R_id_temp2"


class RIdTemp3(models.Model):
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "R_id_temp3"


class RUsermailingTest(models.Model):
    id = models.BigAutoField(primary_key=True)
    mailing_id = models.IntegerField()
    user_id = models.IntegerField()
    subject_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "R_usermailing_test"
        unique_together = (("mailing_id", "user_id"),)


class RUsersAlter(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    prefix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    subscription_status = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=249)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    lang_id = models.IntegerField(blank=True, null=True)
    rand_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "R_users_alter"


class RUsersAlter2(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    prefix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    subscription_status = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=249)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    lang_id = models.IntegerField(blank=True, null=True)
    rand_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "R_users_alter2"


class RUsersAlter3(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    prefix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    subscription_status = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=249)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    lang_id = models.IntegerField(blank=True, null=True)
    rand_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "R_users_alter3"


class RUsersAlter4(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    prefix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    subscription_status = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=249)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    lang_id = models.IntegerField(blank=True, null=True)
    rand_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "R_users_alter4"


class RUsersAlter5(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    prefix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    subscription_status = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=249)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    lang_id = models.IntegerField(blank=True, null=True)
    rand_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "R_users_alter5"


class RUsersAlter6(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    prefix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    subscription_status = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=249)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    lang_id = models.IntegerField(blank=True, null=True)
    rand_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "R_users_alter6"


class RUsersAlter7(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    prefix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    subscription_status = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=249)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    lang_id = models.IntegerField(blank=True, null=True)
    rand_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "R_users_alter7"


class AdhocSpamCheckLog(models.Model):
    action_id = models.IntegerField(primary_key=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    result = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "adhoc_spamchecklog"


class AxesAccessLog(models.Model):
    user_agent = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=39, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    http_accept = models.CharField(max_length=1025)
    path_info = models.CharField(max_length=255)
    attempt_time = models.DateTimeField()
    logout_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "axes_accesslog"


class CoreGoogleOauthCredentials(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    staff_user_id = models.IntegerField()
    credentials = models.TextField()
    email = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_googleoauthcredentials"


class CoreInconsistentTransactions(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type = models.CharField(max_length=255)
    order_id = models.IntegerField()
    account = models.CharField(max_length=255)
    test_mode = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    success = models.IntegerField()
    trans_id = models.CharField(max_length=255, blank=True, null=True)
    failure_description = models.CharField(max_length=255)
    failure_code = models.CharField(max_length=255, blank=True, null=True)
    failure_message = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "core_inconsistent_transactions"


class CoreLastEngaged(models.Model):
    user = models.OneToOneField(CoreUser, models.DO_NOTHING, primary_key=True)
    days = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = "core_lastengaged"


class CoreMailingset17638(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17638"


class CoreMailingset17725(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17725"


class CoreMailingset17726(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17726"


class CoreMailingset17727(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17727"


class CoreMailingset17728(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17728"


class CoreMailingset17729(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17729"


class CoreMailingset17730(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17730"


class CoreMailingset17731(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17731"


class CoreMailingset17732(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17732"


class CoreMailingset17733(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17733"


class CoreMailingset17734(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17734"


class CoreMailingset17735(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17735"


class CoreMailingset17736(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17736"


class CoreMailingset17737(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17737"


class CoreMailingset17738(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17738"


class CoreMailingset17739(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17739"


class CoreMailingset17740(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17740"


class CoreMailingset17741(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17741"


class CoreMailingset17742(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17742"


class CoreMailingset17743(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17743"


class CoreMailingset17744(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17744"


class CoreMailingset17745(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17745"


class CoreMailingset17746(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17746"


class CoreMailingset17747(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17747"


class CoreMailingset17748(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17748"


class CoreMailingset17749(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17749"


class CoreMailingset17750(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17750"


class CoreMailingset17751(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17751"


class CoreMailingset17752(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17752"


class CoreMailingset17753(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17753"


class CoreMailingset17754(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17754"


class CoreMailingset17755(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17755"


class CoreMailingset17756(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17756"


class CoreMailingset17757(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17757"


class CoreMailingset17758(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17758"


class CoreMailingset17759(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17759"


class CoreMailingset17760(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17760"


class CoreMailingset17761(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17761"


class CoreMailingset17762(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17762"


class CoreMailingset17763(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17763"


class CoreMailingset17764(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17764"


class CoreMailingset17765(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17765"


class CoreMailingset17855(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17855"


class CoreMailingset17856(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17856"


class CoreMailingset17857(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17857"


class CoreMailingset17858(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17858"


class CoreMailingset17859(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17859"


class CoreMailingset17860(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17860"


class CoreMailingset17861(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "core_mailingset_17861"


class CoreModelAdminDefaults(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    initial_values_json = models.TextField()

    class Meta:
        managed = False
        db_table = "core_modeladmindefaults"


class CoreTargetingEventField(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    targeting = models.ForeignKey(CoreMailingTargeting, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    values = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "core_targetingeventfield"


class CoreUploadUndoSkipped(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    upload = models.ForeignKey(CoreUpload, models.DO_NOTHING)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "core_uploadundoskipped"


class CoreUploadUser(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    upload = models.ForeignKey(CoreUpload, models.DO_NOTHING)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    created_user = models.IntegerField()

    class Meta:
        managed = False
        db_table = "core_uploaduser"


class CoreUsermailing2009(models.Model):
    id = models.IntegerField(primary_key=True)
    mailing_id = models.IntegerField()
    user_id = models.IntegerField()
    subject_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_usermailing_2009"


class CoreUsermailing2010(models.Model):
    id = models.IntegerField(primary_key=True)
    mailing_id = models.IntegerField()
    user_id = models.IntegerField()
    subject_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_usermailing_2010"


class CoreUsermailing2011(models.Model):
    id = models.IntegerField(primary_key=True)
    mailing_id = models.IntegerField()
    user_id = models.IntegerField()
    subject_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_usermailing_2011"


class CoreUsermailing2012(models.Model):
    id = models.IntegerField(primary_key=True)
    mailing_id = models.IntegerField()
    user_id = models.IntegerField()
    subject_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_usermailing_2012"


class CoreUsermailing2013(models.Model):
    id = models.IntegerField(primary_key=True)
    mailing_id = models.IntegerField()
    user_id = models.IntegerField()
    subject_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_usermailing_2013"


class CoreUsermailing2014(models.Model):
    id = models.IntegerField(primary_key=True)
    mailing_id = models.IntegerField()
    user_id = models.IntegerField()
    subject_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_usermailing_2014"


class CoreUsermailing2015(models.Model):
    id = models.IntegerField(primary_key=True)
    mailing_id = models.IntegerField()
    user_id = models.IntegerField()
    subject_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "core_usermailing_2015"


class EventsCampaignAlsoSearchCampaigns(models.Model):
    from_campaign = models.ForeignKey(
        EventsCampaign, models.DO_NOTHING, related_name="campaigns_from"
    )
    to_campaign = models.ForeignKey(
        EventsCampaign, models.DO_NOTHING, related_name="campaigns_to"
    )

    class Meta:
        managed = False
        db_table = "events_campaign_also_search_campaigns"
        unique_together = (("from_campaign", "to_campaign"),)


class LabVariationcustomfield(models.Model):
    variation = models.ForeignKey(LabVariation, models.DO_NOTHING)
    name = models.ForeignKey(CoreAllowedPageField, models.DO_NOTHING, db_column="name")
    value = models.TextField()

    class Meta:
        managed = False
        db_table = "lab_variationcustomfield"


class MergeFile33(models.Model):
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    testing = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "mergefile_33"


class OneClickCookie(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    key = models.CharField(unique=True, max_length=50)
    json = models.TextField()

    class Meta:
        managed = False
        db_table = "oneclick_cookie"


class OneClickCredential(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    internal_name = models.CharField(max_length=255)
    ak_publishable_key = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    provider_publishable_key = models.CharField(max_length=255)
    keys = models.TextField()
    public_name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    pac = models.IntegerField()
    require_country = models.IntegerField()
    prefill = models.IntegerField()
    image_path = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "oneclick_credential"


class OtpStaticStaticDevice(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    name = models.CharField(max_length=64)
    confirmed = models.IntegerField()
    throttling_failure_count = models.PositiveIntegerField()
    throttling_failure_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "otp_static_staticdevice"


class OtpStaticStaticToken(models.Model):
    device = models.ForeignKey(OtpStaticStaticDevice, models.DO_NOTHING)
    token = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = "otp_static_statictoken"


class OtpTotpTotpDevice(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    name = models.CharField(max_length=64)
    confirmed = models.IntegerField()
    key = models.CharField(max_length=80)
    step = models.PositiveSmallIntegerField()
    t0 = models.BigIntegerField()
    digits = models.PositiveSmallIntegerField()
    tolerance = models.PositiveSmallIntegerField()
    drift = models.SmallIntegerField()
    last_t = models.BigIntegerField()
    throttling_failure_count = models.PositiveIntegerField()
    throttling_failure_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "otp_totp_totpdevice"


class PmkCoreUser(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255)
    prefix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    subscription_status = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    lang_id = models.IntegerField(blank=True, null=True)
    rand_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pmk_core_user"


class PmkJul14CoreUser(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255)
    prefix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    subscription_status = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    postal = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    plus4 = models.CharField(max_length=4)
    country = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    lang_id = models.IntegerField(blank=True, null=True)
    rand_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pmk_jul14_core_user"


class PmkTest0(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_0"


class PmkTest1(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_1"


class PmkTest10(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_10"


class PmkTest11(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_11"


class PmkTest12(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_12"


class PmkTest13(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_13"


class PmkTest14(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_14"


class PmkTest15(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_15"


class PmkTest16(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_16"


class PmkTest17(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_17"


class PmkTest18(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_18"


class PmkTest19(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_19"


class PmkTest2(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_2"


class PmkTest20(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_20"


class PmkTest21(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_21"


class PmkTest22(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_22"


class PmkTest23(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_23"


class PmkTest24(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_24"


class PmkTest25(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_25"


class PmkTest26(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_26"


class PmkTest27(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_27"


class PmkTest28(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_28"


class PmkTest29(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_29"


class PmkTest3(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_3"


class PmkTest30(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_30"


class PmkTest31(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_31"


class PmkTest4(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_4"


class PmkTest5(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_5"


class PmkTest6(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_6"


class PmkTest7(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_7"


class PmkTest8(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_8"


class PmkTest9(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "pmk_test_9"


class QuickDonateEnrollment(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "quickdonate_enrollment"


class RawMczDemo(models.Model):
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    sequence = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    statefips = models.CharField(max_length=255, blank=True, null=True)
    countyfips = models.CharField(max_length=255, blank=True, null=True)
    percent = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "raw_mcz_demo"


class RawZipSample(models.Model):
    zip = models.CharField(max_length=5)
    c = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "raw_zip_sample"


class ScorePoolLastEngaged(models.Model):
    user = models.OneToOneField(CoreUser, models.DO_NOTHING, primary_key=True)
    days = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = "scorepool_lastengaged"


class ScorePoolListHealth(models.Model):
    scored_at = models.DateField()
    score_type = models.CharField(max_length=255)
    score = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = "scorepool_listhealth"


class ScorePoolUserScore(models.Model):
    user = models.OneToOneField(CoreUser, models.DO_NOTHING, primary_key=True)
    score = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = "scorepool_userscore"


class TextingMessageset32(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "texting_messageset_32"


class TextingMessageset58(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "texting_messageset_58"


class TextingMessageset63(models.Model):
    order_id = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = "texting_messageset_63"


class TigerStateDistrictMigrated(models.Model):
    chamber = models.CharField(primary_key=True, max_length=20)
    tiger_dist = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = "tiger_state_district_migrated"
        unique_together = (("chamber", "tiger_dist"),)


class TwoFactorPhoneDevice(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    name = models.CharField(max_length=64)
    confirmed = models.IntegerField()
    number = models.CharField(max_length=16)
    key = models.CharField(max_length=40)
    method = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = "two_factor_phonedevice"
