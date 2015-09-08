package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

import android.app.Activity;
import android.app.TabActivity;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.SystemClock;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TabHost;
import android.widget.TabHost.TabSpec;
import android.widget.TextView;


/**
 * Created by Ranjan on 19-08-2015.
 */
public class Retailer_Tab_View extends TabActivity implements View.OnClickListener {


    TextView tv_top, tv_rnm, tv_contact;
    ImageView imv_back, imv_save, imv_syn;
    TabHost tabHost;

//Clock Part
    private RelativeLayout rl_bottom;
    TextView Show_timer;
    Button Start,Stop,Pause;
    private long startTime = 0L;
    private Handler customHandler = new Handler();
    long timeInMilliseconds = 0L;
    long timeSwapBuff = 0L;
    long updatedTime = 0L;
    Integer listPosition;

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.retailer_tab_view);

        Bundle extras = getIntent().getExtras();
        if (extras != null) {
            listPosition = extras.getInt("listPosition");
        }

        tabHost = (TabHost) findViewById(android.R.id.tabhost);
        tv_top = (TextView) findViewById(R.id.tv_tittle_bar);
        tv_top.setText(MenuView_Activity.list_content1[listPosition]);
        imv_back = (ImageView) findViewById(R.id.iv_back);
        imv_save = (ImageView) findViewById(R.id.iv_save);
        imv_syn = (ImageView) findViewById(R.id.iv_syn);
        imv_syn.setOnClickListener(this);
        //tabHost.setOnTabChangedListener(this);

        // Clock part
        Start = (Button) findViewById(R.id.btn_start);
        Stop = (Button) findViewById(R.id.btn_stop);
        Pause = (Button) findViewById(R.id.btn_pause);
        Show_timer = (TextView) findViewById(R.id.tv_timer);
        rl_bottom = (RelativeLayout)findViewById(R.id.rl_bottom);

        rl_bottom.setOnClickListener(this);
        imv_back.setOnClickListener(this);
        Stop.setOnClickListener(this);
        Pause.setOnClickListener(this);
        Start.setOnClickListener(this);

        Stop.setVisibility(View.GONE);
        Pause.setVisibility(View.GONE);
        Start.setVisibility(View.GONE);
        Show_timer.setVisibility(View.GONE);



        // Report tab
        Intent intentReport = new Intent().setClass(this, Job_details_view.class);
        TabSpec tabSpecReport = tabHost.newTabSpec("Report");
        tabSpecReport.setIndicator("Report");
        tabSpecReport.setContent(intentReport);

        // OutStanding tab
        Intent intentOutStanding = new Intent().setClass(this, OutSanding_View.class);
        TabSpec tabSpecOutStanding = tabHost.newTabSpec("Outstanding");
        tabSpecOutStanding.setIndicator("Outstanding");
        tabSpecOutStanding.setContent(intentOutStanding);
        //Order Tab
        Intent intentOrder = new Intent().setClass(this, Order_View.class);
        TabHost.TabSpec tabSpecOrder = tabHost.newTabSpec("Order");
        tabSpecOrder.setIndicator("Order");
        tabSpecOrder.setContent(intentOrder);


        // add all tabs

        tabHost.addTab(tabSpecOrder);
        tabHost.addTab(tabSpecOutStanding);
        tabHost.addTab(tabSpecReport);



        //set Windows tab as default (zero based)
        tabHost.setCurrentTab(0);


    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {

            case R.id.iv_syn: {

                startActivity(getIntent());


            }
            break;
            case R.id.iv_back: {
                finish();
                     }
            break;

            case R.id.rl_bottom:
                Stop.setVisibility(View.VISIBLE);
                Pause.setVisibility(View.VISIBLE);
                Show_timer.setVisibility(View.VISIBLE);
                startTime = SystemClock.uptimeMillis();
                customHandler.postDelayed(updateTimerThread, 0);
                Stop.setEnabled(true);
                Pause.setEnabled(true);
                rl_bottom.setBackgroundDrawable(getResources().getDrawable(R.drawable.onchangebg));

                break;

            case R.id.btn_start:
                startTime = SystemClock.uptimeMillis();
                customHandler.postDelayed(updateTimerThread, 0);
                Stop.setEnabled(true);
                Pause.setEnabled(true);
                Pause.setVisibility(View.VISIBLE);
                break;

            case R.id.btn_stop:
                //Show_timer=null;
                timeSwapBuff += timeInMilliseconds;
                customHandler.removeCallbacks(updateTimerThread);
                Pause.setVisibility(View.GONE);
                Start.setVisibility(View.GONE);
                //Disable the pause, resume and cancel button
                //Start.setEnabled(true);
                //Start.setVisibility(View.VISIBLE);
                break;

            case R.id.btn_pause:
                timeSwapBuff += timeInMilliseconds;
                customHandler.removeCallbacks(updateTimerThread);
                Start.setEnabled(true);
                Stop.setEnabled(true);
                Start.setVisibility(View.VISIBLE);
                Stop.setVisibility(View.VISIBLE);


            default:
                break;

        }

    }

    private Runnable updateTimerThread = new Runnable() {

        public void run() {

            timeInMilliseconds = SystemClock.uptimeMillis() - startTime;

            updatedTime = timeSwapBuff + timeInMilliseconds;

            int secs = (int) (updatedTime / 1000);
            int mins = secs / 60;
            secs = secs % 60;
            int milliseconds = (int) (updatedTime % 1000);
            Show_timer.setText("" + mins + ":"
                    + String.format("%02d", secs) + ":"
                    + String.format("%03d", milliseconds));
            customHandler.postDelayed(this, 0);
        }

    };

}
