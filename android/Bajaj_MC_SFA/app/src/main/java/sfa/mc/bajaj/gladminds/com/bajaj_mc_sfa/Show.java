package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.ImageView;

import java.io.File;

/**
 * Created by Ranjan on 23-08-2015.
 */
public class Show extends Activity {

    ImageView imv_back;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.ada);


        imv_back = (ImageView) findViewById(R.id.showImg);

        File imgFile = new  File("sdcard/sdcard/StoryBook/Cutomer.jpeg");

        if(imgFile.exists()){

            Bitmap myBitmap = BitmapFactory.decodeFile(imgFile.getAbsolutePath());
            imv_back.setImageBitmap(myBitmap);

        }

    }
}
