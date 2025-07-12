# authentication
languages = {
    "en",
    # English language
    "ar"
    # Arabic language
}

messages = {
    "authentication": {
        # class
        "SignIn": {
            # fun
            "check_password": {
                "none": {
                    "en": "Please enter your name",
                    "ar": "من فضلك أدخل إسمك"
                },
                "too_weak": {
                    "en": "Password is too weak",
                    "ar": "كلمة المرور ضعيفة جدا"
                },
                "too_big": {
                    "en": "Password is too big",
                    "ar": "كلمة المرور كبيرة جدًا"
                },
                "pass_old": {
                    "en": "You entered an old password that was changed on a date:",
                    "ar": "لقد أدخلت كلمة مرور قديمة تم تغييرها في تاريخ:"
                },
                "incorrect": {
                    "en": "The password is incorrect",
                    "ar": "كلمة المرور غير صحيحة"
                }
            },
            "check_image": {
                "none": {
                    "en": "please attach picture",
                    "ar": "يرجى إرفاق صورة أخرى"
                },
                "err_image_format": {
                    "en": "Picture format not recognized, please attach another picture",
                    "ar": "لم يتم التعرف على تنسيق الصورة ، يرجى إرفاق صورة أخرى"
                },
            }
        },
        "SignUp": {
            "login_success": {
                "en": "You are logged in successfully",
                "ar": "لقد قمت بتسجيل الدخول بنجاح"
            },
            "check_name": {
                "none": {
                    "en": "Please enter your name",
                    "ar": "من فضلك أدخل إسمك"
                },
                "name_none": {
                    "en": " did not send your name",
                    "ar": " لم ترسل اسمك"
                },
                "min": {
                    "en": "Your name is too small, it should be more than two letters",
                    "ar": "اسمك صغير جدًا ، يجب أن يكون أكثر من حرفين"
                },
                "max": {
                    "en": "Your name is too big, it should be less than 30 characters",
                    "ar": "اسمك كبير جدًا ، يجب أن يكون اقل من 30 حرف"
                }
            },
            "check_birth_date": {
                "none": {
                    "en": "Please add your date of birth",
                    "ar": "برجاء اضافة تاريخ ميلادك"
                },
                "illogical": {
                    "en": "Age is illogical",
                    "ar": "العمر غير منطقي"
                },
                "Invalid": {
                    "en": "Invalid date format (YYYY-MM-DD)",
                    "ar": "تنسيق التاريخ غير صحيح (YYYY-MM-DD)"
                },
            },
            "check_email": {
                "none": {
                    "en": "Please enter your email",
                    "ar": "من فضلك أدخل بريدك الإلكتروني"
                },
                "social_none": {
                    "en": " did not send your email",
                    "ar": " لم ترسل البريد الإلكتروني الخاص بك"
                },
                "min": {
                    "en": "Your email is very small, it should be more than 8 characters",
                    "ar": "بريدك الإلكتروني صغير جدًا ، يجب أن يكون أكثر 8 حروف"
                },
                "max": {
                    "en": "Your email is too big, it should be less than 50 characters",
                    "ar": "بريدك الإلكتروني كبير جدًا ، يجب أن يكون اقل من ٥٠ حرف"
                },
                "already_exists": {
                    "en": "Sorry, this email is owned by someone else",
                    "ar": "عفوا ، هذا البريد الإلكتروني مملوك من قبل شخص آخر"
                },
                "incorrect": {
                    "en": "This email is incorrect",
                    "ar": "هذا البريد الإلكتروني غير صحيح"
                }

            },
            "check_password": {
                "none": {
                    "en": "Please enter the password",
                    "ar": "من فضلك ادخل كلمة السر"
                },
                "min": {
                    "en": "The password is very small, it must be more than 8 letters or numbers",
                    "ar": "كلمة المرور صغيرة جدًا ، يجب أن تكون أكثر من 8 أحرف أو أرقام"
                },
                "max": {
                    "en": "The password is too large, it must be less than 50 characters or numbers",
                    "ar": "كلمة المرور كبيرة جدًا ، يجب أن تكون اقل من ٥٠  حرف أو رقام"
                },
                "lowercase": {
                    "en": "Password must contain at least one lowercase letter.",
                    "ar": "كلمة المرور يجب أن تحتوي على حرف صغير واحد على الأقل"
                },
                "capital": {
                    "en": "Password must contain at least one capital letter.",
                    "ar": "كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل"
                },
                "number": {
                    "en": "Password must contain at least one number",
                    "ar": "كلمة المرور يجب أن تحتوي على رقم واحد على الأقل"
                },
                "special": {
                    "en": "The password must contain at least one special character.",
                    "ar": "كلمة المرور يجب أن تحتوي على رمز خاص واحد على الأقل"
                },

                "name_in": {
                    "en": "To protect your account, please do not enter your name in the password",
                    "ar": "لحماية حسابك ، يرجى عدم إدخال اسمك في كلمة المرور"
                },
                "email_in": {
                    "en": "To protect your account, please do not enter your email in the password",
                    "ar": "لحماية حسابك ، يرجى عدم إدخال بريدك الإلكتروني في كلمة المرور"
                },
                "arabic": {
                    "ar": "كلمة المرور لا يجب أن تحتوي على أحرف عربية.",
                    "en": "Password must not contain Arabic letters."
                },
                "tashkeel": {
                    "ar": "كلمة المرور لا يجب أن تحتوي على تشكيل عربي.",
                    "en": "Password must not contain Arabic diacritics (tashkeel)."
                },
                "space": {
                    "ar": "لا تنس بالمسافات في كلمة المرور.",
                    "en": "Don't forget the spaces in your password."
                }
            },
            "check_provider": {
                "none": {
                    "en": "This social media service provider is not working at the moment",
                    "ar": "مزود خدمة الوسائط الاجتماعية هذا لا يعمل في الوقت الحالي"
                }
            },
            "check_uid": {
                "else_provider": {
                    "en": "Your account is opened by logging in with ",
                    "ar": "يتم فتح حسابك بواسطة تسجيل الدخول با "
                },
                "none": {
                    "en": "You have never created an account with ",
                    "ar": "لم يسبق لك انشاء حساب من خلال "
                }
            },
            "verified": {
                "not_found": {
                    "en": "The email was not found",
                    "ar": "لم يتم العثور على البريد الإلكتروني"
                },
                "already_verified": {
                    "en": "This email has already been verified",
                    "ar": "تم التحقق من هذا البريد الالكتروني سابقا"
                },
                "none_code": {
                    "en": "Please enter the verification code",
                    "ar": "الرجاء إدخال رمز التحقق"
                },
                "not_equal_code": {
                    "en": "Verification code must be 6 digits",
                    "ar": "يجب أن يتكون رمز التحقق من 6 أرقام"
                },
                "Invalid": {
                    "en": "Invalid verification code",
                    "ar": "رمز التحقق غير صحيح"
                },
                "successfully": {
                    "en": "The email has been confirmed successfully",
                    "ar": "تم تأكيد البريد الإلكتروني بنجاح"
                }
            },

        },
        "ForgotPassword": {
            "check_code": {
                "successfully": {
                    "en": "Code Verified Successfully",
                    "ar": "تم التحقق من الرمز بنجاح "
                },
                "code_is_incorrect": {
                    "en": "The code is incorrect",
                    "ar": "الرمز غير صحيح"
                }
            },
            "check_send": {
                "sending_email": {
                    "en": "A verification code has been sent to your email",
                    "ar": "تم إرسال رمز التحقق إلى بريدك الإلكتروني"
                },
                "sending_mobile": {
                    "en": "Verification code has been sent to the phone number via SMS",
                    "ar": "تم إرسال رمز التحقق إلى رقم الهاتف عبر الرسائل القصيرة"
                },
                "not_sending_email": {
                    "en": "The code cannot be re-sent before the remaining time expires",
                    "ar": "لا يمكن إعادة إرسال الرمز قبل انتهاء الوقت المتبقي"
                },
                "err_account_type": {
                    "en": "Your account cannot use this link",
                    "ar": "لا يمكن لحسابك استخدام هذا الرابط"
                }
            },
            "check_new_pass": {
                "successfully": {
                    "en": "Code Verified Successfully",
                    "ar": "تم التحقق من الرمز بنجاح "
                },
                "code_is_incorrect": {
                    "en": "There is an error in credibility",
                    "ar": "هناك خطأ في المصداقية"
                }
            },
            "change_pass": {
                "old_incorrect": {
                    "en": "The old password is incorrect",
                    "ar": "كلمة المرور القديمة غير صحيحة"
                },
                "pass_check": {
                    "none": {
                        "en": "Please enter the new password",
                        "ar": "الرجاء إدخال كلمة المرور الجديدة"
                    },
                    "min": {
                        "en": "The password is weak, it must be more than 6 characters",
                        "ar": "كلمة السر ضعيفة يجب ان تكون اكثر من ٦ احرف"
                    },
                    "max": {
                        "en": "Password is large, must be less than 20 characters",
                        "ar": "كلمة المرور كبيرة ، يجب أن تكون أقل من 20 حرفًا"
                    }
                },
                "old_new_equal": {
                    "en": "Please use a password that you have not set before",
                    "ar": "الرجاء استخدام كلمة مرور لم تقم بتعيينها من قبل"
                },
                "old_new_exactly": {
                    "en": "The new password cannot be exactly the same as the current password",
                    "ar": "لا يمكن أن تكون كلمة المرور الجديدة مطابقة تماما لكلمة المرور الحالية"
                },
                "successfully": {
                    "en": "Password has been updated successfully",
                    "ar": "تم تحديث كلمة السر بنجاح"
                }
            },
            "create_pass": {
                "successfully": {
                    "en": "Code Verified Successfully",
                    "ar": "تم التحقق من الرمز بنجاح "
                },
                "use_session": {
                    "en": "This session has been used before, can not use it again",
                    "ar": "تم استخدام هذه الجلسة من قبل ، ولا يمكن استخدامها مرة أخرى"
                },
                "session_expired": {
                    "en": "This session has expired, this link is not working anymore",
                    "ar": "انتهت هذه الجلسة ، هذا الرابط لا يعمل بعد الآن"
                },
                "block_session_new_pass": {
                    "en": "You are using a session that does not have permission to create your account password",
                    "ar": "أنت تستخدم جلسة ليس لديها إذن لإنشاء كلمة مرور حسابك"
                },
                "session_not_found": {
                    "en": "This link is not recognized",
                    "ar": "لم يتم التعرف علي هذا الرابط"
                },
                "old_pass": {
                    "en": "You cannot enter the password you created before",
                    "ar": "لا يمكنك إدخال كلمة المرور قمت بإنشائها من قبل"
                }
            }
        }
    },
    "validation_code": {
        "send_code_email": {

            "sending_email": {
                "en": "A verification code has been sent to your email",
                "ar": "تم إرسال رمز التحقق إلى بريدك الإلكتروني"
            },
            "block_account": {
                "en": "Sorry, your account is banned from logging in",
                "ar": "عذرا ، تم حظر حسابك من تسجيل الدخول"
            },
            "type_error_sending_email": {
                "en": "The request type is not recognized",
                "ar": "لم يتم التعرف علي نوع الطلب"
            },
            "not_sending_email": {
                "en": "The code cannot be re-sent before the remaining time expires",
                "ar": "لا يمكن إعادة إرسال الرمز قبل انتهاء الوقت المتبقي"
            }

        }
    },

}
