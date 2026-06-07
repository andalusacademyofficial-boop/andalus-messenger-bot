import os
import requests
import google.generativeai as genai
from flask import Flask, request

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-flash-latest")

user_state = {}

REGISTRATION_INFO = (
    "📋 شروط ومتطلبات التسجيل\n\n"
    "✅ شروط القبول:\n"
    "- مؤهل دراسي (الثانوية بأنواعها - الكليات - قسم خاص للإعدادية)\n"
    "- السن من 18 إلى 40 سنة\n"
    "- لا يشترط سنة التخرج\n\n"
    "📄 المستندات المطلوبة:\n"
    "- صورة البطاقة الشخصية\n"
    "- صورة المؤهل الدراسي\n"
    "- 4 صور شخصية\n"
    "- شهادة الميلاد\n"
    "- ملف الالتحاق من مقر الأكاديمية\n\n"
    "📞 للتسجيل الفوري:\n"
    "01286868182\n"
    "01021004428"
)

CENTER_INFO = (
    "🏥 مركز الأندلس لإعداد وتدريب وتأهيل الكوادر\n\n"
    "صرح تدريبي متخصص في إعداد وتأهيل الكوادر الصحية والإدارية والتقنية.\n\n"
    "🏆 الاعتمادات:\n"
    "✔ معتمد من المعهد القومي للجودة\n"
    "✔ القرار رقم T347/411\n\n"
    "🤖 نفخر بأننا أول مركز تدريب صحي في البحيرة\n"
    "يستخدم الذكاء الاصطناعي في خدمة طلابه.\n\n"
    "📍 مركز الأندلس... حيث يبدأ طريقك نحو التعلم والتميز المهني."
)

HEALTH_ASSISTANT = (
    "🔹 برنامج مساعد خدمات صحية\n\n"
    "النظام الأساسي (9 شهور):\n"
    "💰 7500 جنيه | مقدم 2000\n"
    "➕ 350 فتح ملف + 500 شنطة أدوات\n\n"
    "النظام الاحترافي (12 شهر):\n"
    "💰 10000 جنيه | مقدم 2000\n"
    "➕ 350 فتح ملف + 500 شنطة أدوات\n\n"
    "📞 01286868182"
)

HEALTH_LAB = (
    "🔬 برنامج مساعد فني تحاليل طبية\n\n"
    "⏳ 3 شهور | 💰 3500 جنيه | مقدم 1000\n\n"
    "✔ شهادة معتمدة من جامعة حكومية\n"
    "✔ تدريب عملي على سحب العينات\n\n"
    "📞 01286868182"
)

HEALTH_DENTAL = (
    "🦷 برنامج مساعد طبيب أسنان\n\n"
    "⏳ 3 شهور | 💰 4000 جنيه | مقدم 1000\n\n"
    "✔ شهادة معتمدة من جامعة حكومية\n"
    "✔ تدريب بعيادة أسنان\n\n"
    "📞 01286868182"
)

HEALTH_SECRETARY = (
    "🏥 برنامج السكرتارية الطبية\n\n"
    "⏳ 3 شهور | 💰 3500 جنيه | مقدم 1000\n\n"
    "✔ شهادة معتمدة من جامعة حكومية\n"
    "✔ تدريب إداري طبي\n\n"
    "📞 01286868182"
)

HEALTH_FIRST_AID = (
    "🚑 دورة الإسعافات الأولية\n\n"
    "⏳ يوم مكثف 6-8 ساعات | 💰 500 جنيه\n\n"
    "✔ شهادة حضور معتمدة\n"
    "✔ تدريب عملي CPR\n\n"
    "📞 01286868182"
)

BRANCH_KAFR = (
    "🏢 فرع كفر الدوار\n"
   
    "📞 01286868182\n"
    "📞 01021004428"
)

BRANCH_VIC = (
    "🏢 فرع الإسكندرية - فيكتوريا\n"
    
    "📞 01555654545"
)

BOOKING_MSG = (
    "📅 حجز موعد مع الإدارة\n\n"
    "اكتب بياناتك على الترتيب:\n"
    "1 - اسمك رباعي\n"
    "2 - رقم تليفونك\n"
    "3 - سبب الموعد\n\n"
    "وهنتواصل معاك في أقرب وقت ✅"
)


def send_quick_replies(recipient_id, text, replies):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    quick_replies = [{"content_type": "text", "title": r, "payload": r} for r in replies]
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text, "quick_replies": quick_replies}
    }
    requests.post(url, json=payload)


def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {"recipient": {"id": recipient_id}, "message": {"text": text}}
    requests.post(url, json=payload)


def show_main_menu(sender_id, name=""):
    greeting = "أهلاً " + name + "!\n\n" if name else ""
    send_quick_replies(
        sender_id,
        greeting + "🏥 مركز الاندلس للتدريب\n\n\nاستفساراتك عن إيه؟",
        ["👨‍🎓 متدرب حالي", "📋 تسجيل جديد", "🎓 الكورسات", "🏥 عن المركز", "📍 الفروع", "📅 حجز موعد"]
    )


def show_enrolled_menu(sender_id):
    send_quick_replies(
        sender_id,
        "👨‍🎓 أهلاً بك يا متدرب!\nاختار اللي تحتاجه:",
        ["📚 بوت المناهج", "📅 جدول المحاضرات", "🎓 استفسار شهادة", "🔙 رجوع"]
    )


def show_courses_menu(sender_id):
    send_quick_replies(
        sender_id,
        "🎓 برامج مركز الاندلس:\nاختار المجال:",
        ["🏥 خدمات صحية", "🌍 اللغات", "🧠 صحة نفسية", "🥗 تغذية علاجية", "📊 كورسات إدارية", "💻 تكنولوجيا", "🔙 رجوع"]
    )


def show_health_menu(sender_id):
    send_quick_replies(
        sender_id,
        "🏥 برامج الخدمات الصحية:",
        ["مساعد خدمات صحية", "مساعد تحاليل", "مساعد أسنان", "سكرتارية طبية", "إسعافات أولية", "🔙 رجوع"]
    )


def show_branches_menu(sender_id):
    send_quick_replies(
        sender_id,
        "📍 فروع مركز الأندلس:",
        ["🏢 فرع كفر الدوار", "🏢 فرع الإسكندرية", "🔙 رجوع"]
    )


def handle_message(sender_id, msg, sender_name):
    msg = msg.strip()
    state = user_state.get(sender_id, "main")

    greetings = ["مرحبا", "هلا", "السلام عليكم", "اهلا", "ابدأ", "start", "hi", "hello", "مرحبً"]

    if msg in greetings:
        user_state[sender_id] = "main"
        show_main_menu(sender_id, sender_name)
        return

    if msg == "🔙 رجوع":
        if state in ["enrolled", "courses", "branches", "booking"]:
            user_state[sender_id] = "main"
            show_main_menu(sender_id)
        elif state == "health":
            user_state[sender_id] = "courses"
            show_courses_menu(sender_id)
        elif state == "curriculum":
            user_state[sender_id] = "enrolled"
            show_enrolled_menu(sender_id)
        else:
            user_state[sender_id] = "main"
            show_main_menu(sender_id)
        return

    if state == "main":
        if msg == "👨‍🎓 متدرب حالي":
            user_state[sender_id] = "enrolled"
            show_enrolled_menu(sender_id)
        elif msg == "📋 تسجيل جديد":
            send_message(sender_id, REGISTRATION_INFO)
            show_main_menu(sender_id)
        elif msg == "🎓 الكورسات":
            user_state[sender_id] = "courses"
            show_courses_menu(sender_id)
        elif msg == "🏥 عن المركز":
            send_message(sender_id, CENTER_INFO)
            show_main_menu(sender_id)
        elif msg == "📍 الفروع":
            user_state[sender_id] = "branches"
            show_branches_menu(sender_id)
        elif msg == "📅 حجز موعد":
            user_state[sender_id] = "booking"
            send_message(sender_id, BOOKING_MSG)
        else:
            show_main_menu(sender_id, sender_name)

    elif state == "enrolled":
        if msg == "📚 بوت المناهج":
            user_state[sender_id] = "curriculum"
            send_quick_replies(sender_id, "اكتب سؤالك من المناهج:", ["🔙 رجوع"])
        elif msg == "📅 جدول المحاضرات":
            send_message(sender_id, "للاستفسار عن الجدول:\n📞 01286868182")
            show_enrolled_menu(sender_id)
        elif msg == "🎓 استفسار شهادة":
            send_message(sender_id, "للاستفسار عن الشهادة:\n📞 01286868182\n📞 01021004428")
            show_enrolled_menu(sender_id)
        else:
            show_enrolled_menu(sender_id)

    elif state == "curriculum":
        send_message(sender_id, "بفكر...")
        try:
            response = model.generate_content(
                "أنت مساعد تعليمي لمركز الاندلس للتدريب. أجب بالعربي البسيط:\n\n" + msg
            )
            send_message(sender_id, response.text)
        except Exception:
            send_message(sender_id, "حصل خطأ، حاول تاني.")
        send_quick_replies(sender_id, "عندك سؤال تاني؟", ["🔙 رجوع"])

    elif state == "courses":
        if msg == "🏥 خدمات صحية":
            user_state[sender_id] = "health"
            show_health_menu(sender_id)
        elif msg == "🌍 اللغات":
            send_message(sender_id, "للاستفسار عن كورسات اللغات:\n📞 01286868182")
            show_courses_menu(sender_id)
        elif msg == "🧠 صحة نفسية":
            send_message(sender_id, "للاستفسار عن كورسات الصحة النفسية:\n📞 01286868182")
            show_courses_menu(sender_id)
        elif msg == "🥗 تغذية علاجية":
            send_message(sender_id, "للاستفسار عن كورسات التغذية:\n📞 01286868182")
            show_courses_menu(sender_id)
        elif msg == "📊 كورسات إدارية":
            send_message(sender_id, "للاستفسار عن الكورسات الإدارية:\n📞 01286868182")
            show_courses_menu(sender_id)
        elif msg == "💻 تكنولوجيا":
            send_message(sender_id, "للاستفسار عن كورسات التكنولوجيا:\n📞 01286868182")
            show_courses_menu(sender_id)
        else:
            show_courses_menu(sender_id)

    elif state == "health":
        if msg == "مساعد خدمات صحية":
            send_message(sender_id, HEALTH_ASSISTANT)
            show_health_menu(sender_id)
        elif msg == "مساعد تحاليل":
            send_message(sender_id, HEALTH_LAB)
            show_health_menu(sender_id)
        elif msg == "مساعد أسنان":
            send_message(sender_id, HEALTH_DENTAL)
            show_health_menu(sender_id)
        elif msg == "سكرتارية طبية":
            send_message(sender_id, HEALTH_SECRETARY)
            show_health_menu(sender_id)
        elif msg == "إسعافات أولية":
            send_message(sender_id, HEALTH_FIRST_AID)
            show_health_menu(sender_id)
        else:
            show_health_menu(sender_id)

    elif state == "branches":
        if msg == "🏢 فرع كفر الدوار":
            send_message(sender_id, BRANCH_KAFR)
            show_branches_menu(sender_id)
        elif msg == "🏢 فرع الإسكندرية":
            send_message(sender_id, BRANCH_VIC)
            show_branches_menu(sender_id)
        else:
            show_branches_menu(sender_id)

    elif state == "booking":
        send_message(sender_id, "تم استلام بياناتك:\n\n" + msg + "\n\nهنتواصل معاك في أقرب وقت ✅")
        user_state[sender_id] = "main"
        show_main_menu(sender_id)


@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge
    return "Invalid token", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data.get("object") == "page":
        for entry in data["entry"]:
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                if "message" in event and "text" in event["message"]:
                    msg = event["message"]["text"]
                    try:
                        profile = requests.get(
                            f"https://graph.facebook.com/{sender_id}?fields=first_name&access_token={PAGE_ACCESS_TOKEN}"
                        ).json()
                        name = profile.get("first_name", "")
                    except Exception:
                        name = ""
                    handle_message(sender_id, msg, name)
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
