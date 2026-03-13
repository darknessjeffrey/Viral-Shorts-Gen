import os
import random

# استدعاء المكتبات بالمسار المباشر لتجنب خطأ moviepy.editor
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx

def create_tiktok_clips(video_filename):
    # 1. إعداد مجلد المخرجات
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        # 2. تحميل الفيديو الأساسي
        print(f"--- جاري تحميل الفيديو: {video_filename} ---")
        clip = VideoFileClip(video_filename)
        total_duration = clip.duration
        
        # 3. حساب أبعاد التيك توك (9:16)
        w, h = clip.size
        target_ratio = 9/16
        target_w = h * target_ratio
        
        current_start = 0
        count = 1

        # 4. عملية التقطيع العشوائي (بين 30 و 40 ثانية)
        while current_start + 30 < total_duration:
            duration = random.randint(30, 40)
            end_time = current_start + duration

            # عشان لو وصلنا لآخر الفيديو منعديش الوقت الأصلي
            if end_time > total_duration:
                end_time = total_duration

            print(f"جاري معالجة المقطع رقم {count} (من {current_start} إلى {end_time} ثانية)...")

            # استخراج المقطع الزمني
            sub_clip = clip.subclip(current_start, end_time)
            
            # قص المقطع من المنتصف ليناسب الموبايل
            final_clip = vfx.crop(sub_clip, x_center=w/2, y_center=h/2, width=target_w, height=h)

            # حفظ المقطع
            output_name = os.path.join(output_folder, f"{count}.mp4")
            # إعدادات الريندر (fps=24 لتقليل الحجم وتسريع المعالجة)
            final_clip.write_videofile(output_name, codec="libx264", audio_codec="aac", fps=24)

            current_start = end_time
            count += 1

        print(f"\n✅ تم الانتهاء بنجاح! راجع مجلد: {output_folder}")

    except Exception as e:
        print(f"❌ حدث خطأ أثناء المعالجة: {e}")
    finally:
        # إغلاق الملف لتحرير الذاكرة
        if 'clip' in locals():
            clip.close()

# --- نقطة تشغيل الاسكربت ---
if __name__ == "__main__":
    # تأكد إن الفيديو بتاعك اسمه video.mp4 وموجود في نفس الفولدر
    video_file = "video.mp4" 
    
    if os.path.exists(video_file):
        create_tiktok_clips(video_file)
    else:
        print(f"⚠️ مش قادر ألاقي ملف اسمه '{video_file}' في الفولدر الحالي.")
        print("تأكد إنك حطيت الفيديو في نفس الفولدر وسميته صح.")
