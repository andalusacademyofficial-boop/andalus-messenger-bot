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

MAIN_MENU = (
    "🏥 أهلاً بك في مركز الاندلس للتدريب\n"
    "كفرالدوار — الاسكندرية\n\n"
    "مركز معتمد من المعهد القومي للجودة\n"
    "طبقاً للقرار NQI T 347/411\n\n"
    "استفساراتك عن إيه؟\n\n"
    "1 - أنا متدرب حالي\n"
    "2 - عاوز أسجل في المركز\n"
    "3 - الكورسات والبرامج\n"
    "4 - معلومات عن المركز\n"
    "5 - الفروع والأرقام\n"
    "6 - حجز موعد مع الإدارة"
)

ENROLLED_MENU = (
    "أهلاً بك يا متدرب!\n\n"
    "اختار اللي تحتاجه:\n\n"
    "1 - بوت المناهج\n"
    "2 - جدول المحاضرات\n"
    "3 - استفسار عن الشهادة\n"
    "0 - رجوع للقائمة الرئيسية"
)

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

COURSES_MENU = (
    "🎓 برامج مركز الاندلس للتدريب\n\n"
    "1 - برامج الخدمات الصحية\n"
    "2 - كورسات اللغات\n"
    "3 - كورسات الصحة النفسية\n"
    "4 - كورسات التغذية العلاجية\n"
    "5 - كورسات إدارية\n"
    "6 - كورسات تكنولوجيا وبرمجة وذكاء اصطناعي\n"
    "0 - رجوع للقائمة الرئيسية"
)

HEALTH_MENU = (
    "🏥 برامج الخدمات الصحية\n\n"
    "1 - برنامج مساعد خدمات صحية\n"
    "2 - برنامج مساعد فني تحاليل طبية\n"
    "3 - برنامج مساعد طبيب أسنان\n"
    "4 - برنامج سكرتارية طبية\n"
    "5 - دورات الإسعافات الأولية\n"
    "0 - رجوع"
)

HEALTH_ASSISTANT = (
    "🔹 برنامج مساعد خدمات صحية\n\n"
    "النظام الأساسي (9 شهور):\n"
    "💰 7500 جنيه | مقدم 2000\n"
    "➕ 350 فتح ملف + 500 شنطة أدوات\n"
    "✔ شهادة معتمدة من جامعة حكومية\n"
    "✔ شهادة تدريب مستشفى\n\n"
    "النظام الاحترافي (12 شهر):\n"
    "💰 10000 جنيه | مقدم 2000\n"
    "➕ 350 فتح ملف + 500 شنطة أدوات\n"
    "✔ شهادة موثقة من الخارجية\n"
    "✔ شهادة DataFlow\n"
    "✔ كارنيه مساعد خدمات صحية\n\n"
    "📞 01286868182"
)

HEALTH_LAB = (
    "🔬 برنامج مساعد فني تحاليل طبية\n\n"
    "⏳ مدة البرنامج: 3 شهور\n"
    "💰 3500 جنيه | مقدم 1000\n"
    "➕ 350 فتح ملف + 500 شنطة تدريب\n\n"
    "✔ شهادة معتمدة من جامعة حكومية\n"
    "✔ تدريب عملي على سحب العينات\n"
    "✔ كارنيه متدرب\n\n"
    "📞 01286868182"
)

HEALTH_DENTAL = (
    "🦷 برنامج مساعد طبيب أسنان\n\n"
    "⏳ مدة البرنامج: 3 شهور\n"
    "💰 4000 جنيه | مقدم 1000\n"
    "➕ 350 فتح ملف + 500 شنطة تدريب\n\n"
    "✔ شهادة معتمدة من جامعة حكومية\n"
    "✔ تدريب بعيادة أسنان\n"
    "✔ كارنيه متدرب\n\n"
    "📞 01286868182"
)

HEALTH_SECRETARY = (
    "🏥 برنامج السكرتارية الطبية\n\n"
    "⏳ مدة البرنامج: 3 شهور\n"
    "💰 3500 جنيه | مقدم 1000\n"
    "➕ 350 فتح ملف + 500 شنطة تدريب\n\n"
    "✔ شهادة معتمدة من جامعة حكومية\n"
    "✔ تدريب إداري طبي\n"
    "✔ كارنيه متدرب\n\n"
    "📞 01286868182"
)

HEALTH_FIRST_AID = (
    "🚑 دورة الإسعافات الأولية\n\n"
    "⏳ يوم تدريبي مكثف (6-8 ساعات)\n"
    "💰 500 جنيه\n\n"
    "✔ شهادة حضور معتمدة\n"
    "✔ تدريب عملي CPR\n"
    "✔ مادة علمية مجانية\n\n"
    "📞 01286868182"
)

CENTER_INFO = (
    "🏥 مركز الأندلس لإعداد وتدريب وتأهيل الكوادر\n\n"
    "صرح تدريبي متخصص في إعداد وتأهيل الكوادر الصحية والإدارية والتقنية.\n\n"
    "🏆 الاعتمادات:\n"
    "✔ معتمد من المعهد القومي للجودة\n"
    "✔ القرار رقم T347/411\n\n"
    "🎯 رؤيتنا:\n"
    "أن نكون من المؤسسات الرائدة في مجال التدريب والتأهيل المهني.\n\n"
    "🤖 نفخر بأننا أول مركز تدريب صحي في البحيرة\n"
    "يستخدم الذكاء الاصطناعي في خدمة طلابه.\n\n"
    "📍 مركز الأندلس... حيث يبدأ طريقك نحو التعلم والتميز المهني."
)

BRANCHES_MENU = (
    "📍 فروع مركز الأندلس للتدريب\n\n"
    "1 - فرع كفر الدوار\n"
    "2 - فرع الإسكندرية - فيكتوريا\n"
    "0 - رجوع"
)

BRANCH_KAFR = (
    "🏢 فرع كفر الدوار\n"
    "المقر الرئيسي لمركز الأندلس للتدريب\n"
    "قاعة نادي المعلمين\n\n"
    "📞 للتواصل:\n"
    "01286868182\n"
    "01021004428"
)

BRANCH_VIC = (
    "🏢 فرع الإسكندرية - فيكتوريا\n"
    "قاعة جليم\n\n"
    "📞 للتواصل:\n"
    "01555654545"
)

BOOKING_MSG = (
    "📅 حجز موعد مع الإدارة\n\n"
    "اكتب بياناتك على الترتيب:\n"
    "1 - اسمك رباعي\n"
    "2 - رقم تليفونك\n"
    "3 - سبب الموعد\n\n"
    "وهنتواصل معاك في أقرب وقت"
)


def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post(url, json=payload)


def handle_message(sender_id, msg, sender_name):
    msg = msg.strip()
    state = user_state.get(sender_id, "main")

    greetings = ["مرحبا", "هلا", "السلام عليكم", "اهلا", "ابدأ", "start", "مرحبً", "hi", "hello"]

    if msg in greetings or msg == "0" and state == "main":
        user_state[sender_id] = "main"
        send_message(sender_id, "أهلاً " + sender_name + "!\n\n" + MAIN_MENU)
        return

    if state == "main":
        if msg == "1":
            user_state[sender_id] = "enrolled"
            send_message(sender_id, ENROLLED_MENU)
        elif msg == "2":
            send_message(sender_id, REGISTRATION_INFO)
        elif msg == "3":
            user_state[sender_id] = "courses"
            send_message(sender_id, COURSES_MENU)
        elif msg == "4":
            send_message(sender_id, CENTER_INFO)
        elif msg == "5":
            user_state[sender_id] = "branches"
            send_message(sender_id, BRANCHES_MENU)
        elif msg == "6":
            user_state[sender_id] = "booking"
            send_message(sender_id, BOOKING_MSG)
        else:
            user_state[sender_id] = "main"
            send_message(sender_id, "أهلاً " + sender_name + "!\n\n" + MAIN_MENU)

    elif state == "enrolled":
        if msg == "0":
            user_state[sender_id] = "main"
            send_message(sender_id, MAIN_MENU)
        elif msg == "1":
            user_state[sender_id] = "curriculum"
            send_message(sender_id, "اكتب سؤالك من المناهج وهرد عليك فوراً\n\nاكتب 0 للرجوع.")
        elif msg == "2":
            send_message(sender_id, "📅 جدول المحاضرات\n\nللاستفسار عن الجدول تواصل معنا:\n01286868182")
        elif msg == "3":
            send_message(sender_id, "🎓 للاستفسار عن الشهادة تواصل معنا:\n01286868182\n01021004428")
        else:
            user_state[sender_id] = "main"
            send_message(sender_id, MAIN_MENU)

    elif state == "curriculum":
        if msg == "0":
            user_state[sender_id] = "enrolled"
            send_message(sender_id, ENROLLED_MENU)
        else:
            send_message(sender_id, "بفكر...")
            try:
                response = model.generate_content(
                    "أنت مساعد تعليمي لمركز الاندلس للتدريب. أجب على سؤال الطالب بالعربي البسيط:\n\n" + msg
                )
                send_message(sender_id, response.text)
            except Exception as e:
                send_message(sender_id, "حصل خطأ، حاول تاني.")

    elif state == "courses":
        if msg == "0":
            user_state[sender_id] = "main"
            send_message(sender_id, MAIN_MENU)
        elif msg == "1":
            user_state[sender_id] = "health"
            send_message(sender_id, HEALTH_MENU)
        elif msg == "2":
            send_message(sender_id, "للاستفسار عن كورسات اللغات:\n📞 01286868182")
        elif msg == "3":
            send_message(sender_id, "للاستفسار عن كورسات الصحة النفسية:\n📞 01286868182")
        elif msg == "4":
            send_message(sender_id, "للاستفسار عن كورسات التغذية العلاجية:\n📞 01286868182")
        elif msg == "5":
            send_message(sender_id, "للاستفسار عن الكورسات الإدارية:\n📞 01286868182")
        elif msg == "6":
            send_message(sender_id, "للاستفسار عن كورسات التكنولوجيا والذكاء الاصطناعي:\n📞 01286868182")
        else:
            user_state[sender_id] = "main"
            send_message(sender_id, MAIN_MENU)

    elif state == "health":
        if msg == "0":
            user_state[sender_id] = "courses"
            send_message(sender_id, COURSES_MENU)
        elif msg == "1":
            send_message(sender_id, HEALTH_ASSISTANT)
        elif msg == "2":
            send_message(sender_id, HEALTH_LAB)
        elif msg == "3":
            send_message(sender_id, HEALTH_DENTAL)
        elif msg == "4":
            send_message(sender_id, HEALTH_SECRETARY)
        elif msg == "5":
            send_message(sender_id, HEALTH_FIRST_AID)
        else:
            user_state[sender_id] = "main"
            send_message(sender_id, MAIN_MENU)

    elif state == "branches":
        if msg == "0":
            user_state[sender_id] = "main"
            send_message(sender_id, MAIN_MENU)
        elif msg == "1":
            send_message(sender_id, BRANCH_KAFR)
        elif msg == "2":
            send_message(sender_id, BRANCH_VIC)
        else:
            user_state[sender_id] = "main"
            send_message(sender_id, MAIN_MENU)

    elif state == "booking":
        if msg == "0":
            user_state[sender_id] = "main"
            send_message(sender_id, MAIN_MENU)
        else:
            send_message(sender_id, "تم استلام بياناتك:\n\n" + msg + "\n\nهنتواصل معاك في أقرب وقت.")
            user_state[sender_id] = "main"


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
