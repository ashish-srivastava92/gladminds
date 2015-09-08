package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.ActivityNotFoundException;
import android.content.ContentValues;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.PopupMenu;
import android.widget.RelativeLayout;
import android.widget.TabHost;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;

/**
 * Created by Ranjan on 23-08-2015.
 */
public class Report_view extends AppCompatActivity implements View.OnClickListener {


    static  TextView tv_job,tv_note,tv_note2,tv_job_status,tv_job_status2,tv_attachment_2,imageDetails,tv_equip2,tv_add1,tv_add2,tv_contact1,tv_contact2;

    ImageView imv_attach,show_cutomer_sig,show_my_sig,delete_attach;
    TabHost tabHost;

    private LinearLayout  ll_notes, ll_job_report, ll_customer_sig,ll_my_sig;
    private RelativeLayout ll_HR_OPN1,ll_attachment,ll_c_signature,ll_my_singature;

    final static int CAPTURE_IMAGE_ACTIVITY_REQUEST_CODE = 1;


    Uri imageUri= null;
    public  static ImageView showImg  = null;
    Report_view CameraActivity = null;
    int click=1;

    //New capture work done here

    protected String _path;
    protected boolean _taken;

    protected static final String PHOTO_TAKEN	= "photo_taken";



    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.report_view);
        CameraActivity = this;


        imv_attach = (ImageView) findViewById(R.id.imv_attach);
        showImg = (ImageView) findViewById(R.id.showImg);
        show_cutomer_sig = (ImageView) findViewById(R.id.show_cutomer_sig);
        show_my_sig = (ImageView) findViewById(R.id.show_my_sig);

        tv_job = (TextView) findViewById(R.id.tv_hr_operation1);
        tv_note = (TextView) findViewById(R.id.tv_hr_operation2);
        tv_note2 = (TextView) findViewById(R.id.tv_opn_time2);
        tv_job_status = (TextView) findViewById(R.id.tv_hr_operation4);
        //imageDetails = (TextView) findViewById(R.id.imageDetails);

        tv_job_status2 = (TextView) findViewById(R.id.tv_opn_time4);
        tv_attachment_2 = (TextView) findViewById(R.id.tv_ph_number);
        tv_equip2 = (TextView) findViewById(R.id.tv_opn_time5);


        imv_attach.setOnClickListener(this);
        ll_HR_OPN1 = (RelativeLayout)findViewById(R.id.ll_HR_OPN1);
        ll_attachment = (RelativeLayout)findViewById(R.id.ll_attachment);
        ll_notes = (LinearLayout)findViewById(R.id.ll_HR_OPN2);
        ll_job_report = (LinearLayout)findViewById(R.id.ll_HR_OPN4);
        ll_c_signature = (RelativeLayout)findViewById(R.id.ll_HR_OPN6);
        ll_my_singature = (RelativeLayout)findViewById(R.id.ll_HR_OPN7);
        ll_customer_sig = (LinearLayout)findViewById(R.id.ll_customer_sig);
        ll_my_sig = (LinearLayout)findViewById(R.id.ll_my_sig);


        ll_notes.setOnClickListener(this);
        ll_job_report.setOnClickListener(this);
        ll_c_signature.setOnClickListener(this);
        ll_my_singature.setOnClickListener(this);
        ll_customer_sig.setOnClickListener(this);
        ll_my_sig.setOnClickListener(this);
        ll_HR_OPN1.setOnClickListener(this);
        ll_attachment.setOnClickListener(this);


        ll_my_sig.setVisibility(View.GONE);
        ll_customer_sig.setVisibility(View.GONE);



        _path = Environment.getExternalStorageDirectory() + "/Philips/make_machine_example.jpg";


    }

    @Override
    public void onClick(View v)
    {

        switch(v.getId())
        {


            case R.id.ll_HR_OPN1:

                    ll_notes.setVisibility(View.VISIBLE);
                    ll_job_report.setVisibility(View.VISIBLE);

                break;
            case R.id.ll_HR_OPN4:
                Pop_up_first customizeDialog2 = new Pop_up_first(Report_view.this);
                customizeDialog2.show();
                break;

            case R.id.ll_customer_sig:
                File imgFile1= new File("/sdcard/Philips/Customer.jpeg");
                if(imgFile1.exists()) {
                    ll_customer_sig.setVisibility(View.VISIBLE);

                    Bitmap myBitmap = BitmapFactory.decodeFile(imgFile1.getAbsolutePath());

                    //ImageView myImage = (ImageView) findViewById(R.id.show_cutomer_sig);

                    show_cutomer_sig.setImageBitmap(myBitmap);


                }
                break;
            case R.id.ll_my_sig:
                File imgFile2 = new File("/sdcard/Philips/Mysignature.jpeg");
                if(imgFile2.exists()){
                    ll_my_sig.setVisibility(View.VISIBLE);

                    Bitmap myBitmap = BitmapFactory.decodeFile(imgFile2.getAbsolutePath());

                    //ImageView myImage = (ImageView) findViewById(R.id.show_cutomer_sig);

                    show_my_sig.setImageBitmap(myBitmap);

                }
                break;
            case R.id.ll_HR_OPN2:

                Pop_up_notes customizeDialog_notes = new Pop_up_notes(Report_view.this);
                customizeDialog_notes.show();
                break;

            case R.id.ll_HR_OPN6:


                    ll_customer_sig.setVisibility(View.VISIBLE);
                    Intent myIntent = new Intent(getApplicationContext(), CaptureSignature.class);
                    myIntent.putExtra("Signature", "Customer");
                    startActivity(myIntent);





                break;

            case R.id.imv_attach:
            {

                PopupMenu popup = new PopupMenu(Report_view.this, imv_attach);
                //Inflating the Popup using xml file
                popup.getMenuInflater().inflate(R.menu.menu_pop_up, popup.getMenu());

                //registering popup with OnMenuItemClickListener
                popup.setOnMenuItemClickListener(new PopupMenu.OnMenuItemClickListener() {
                    public boolean onMenuItemClick(MenuItem item) {
                        switch (item.getItemId()) {
                            case R.id.item_images:
                                Toast.makeText(Report_view.this,"You Clicked : " + item.getTitle(),Toast.LENGTH_SHORT).show();
                                return true;
                            case R.id.item_camera:
                                /** Photo capture **/
                                startCameraActivity();
                                return true;
                            case R.id.item_barcode:
                                Toast.makeText(Report_view.this,"You Clicked : " + item.getTitle(),Toast.LENGTH_SHORT).show();
                                return true;
                        }
                        return true;
                    }
                });

                popup.show();//showing popup menu
            }

            break;

            case R.id.ll_HR_OPN7:

                ll_my_sig.setVisibility(View.VISIBLE);
                Intent myIntent_sig = new Intent(getApplicationContext(), CaptureSignature.class);
                myIntent_sig.putExtra("Signature", "Mysignature");
                startActivity(myIntent_sig);


                break;




            default:
                break;
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main_view, menu);
        return true;
    }


    protected void startCameraActivity()
    {
        Log.i("MakeMachine", "startCameraActivity()");
        File file = new File( _path );
        Uri outputFileUri = Uri.fromFile( file );

        Intent intent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE );
        intent.putExtra( MediaStore.EXTRA_OUTPUT, outputFileUri );

        startActivityForResult( intent, 0 );
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data)
    {
        Log.i( "MakeMachine", "resultCode: " + resultCode );
        switch( resultCode )
        {
            case 0:
                Log.i( "MakeMachine", "User cancelled" );
                break;

            case -1:
                onPhotoTaken();
                break;
        }
    }

    protected void onPhotoTaken()
    {
        Log.i( "MakeMachine", "onPhotoTaken" );

        _taken = true;

        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inSampleSize = 4;

        Bitmap bitmap = BitmapFactory.decodeFile( _path, options );

        showImg.setImageBitmap(bitmap);

    }

    @Override
    protected void onRestoreInstanceState( Bundle savedInstanceState){
        Log.i( "MakeMachine", "onRestoreInstanceState()");
        if( savedInstanceState.getBoolean( Report_view.PHOTO_TAKEN ) ) {
            onPhotoTaken();
        }
    }

    @Override
    protected void onSaveInstanceState( Bundle outState ) {
        outState.putBoolean(Report_view.PHOTO_TAKEN, _taken);
    }
}
