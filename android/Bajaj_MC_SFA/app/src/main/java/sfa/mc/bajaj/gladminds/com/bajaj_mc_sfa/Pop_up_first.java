package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

/**
 * Created by Ranjan on 23-08-2015.
 */

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.RadioButton;

public class Pop_up_first extends Dialog implements android.view.View.OnClickListener
{
    //	private static final int MODE_PRIVATE = 0;
    Activity context;
    Button btn_cancel, btn_order;
    static String order_option="";
    //	private RadioGroup radioOrderGroup;
    RadioButton radio_none,radio_yes,radio_no;

    //	public Event_mail(Context context, String desc, String title, String strt_time, String nd_time) {
    public Pop_up_first(Context context) {
        super(context);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.customize_pop_up);
        this.context = (Activity) context;

        order_option="None";

        btn_cancel = (Button)findViewById(R.id.btn_cancle);
        btn_order=(Button)findViewById(R.id.btn_confirm);

        // Name.setInputType(InputType.TYPE_CLASS_TEXT);

//	    radioOrderGroup = (RadioGroup) findViewById(R.id.order);
        radio_none = (RadioButton)findViewById(R.id.radio_None);
        radio_yes= (RadioButton)findViewById(R.id.radio_Yes);
        radio_no=(RadioButton)findViewById(R.id.radio_No);


        radio_none.setOnClickListener(this);
        radio_yes.setOnClickListener(this);
        radio_no.setOnClickListener(this);



        btn_cancel.setOnClickListener(this);
        btn_order.setOnClickListener(this);



    }


    @Override
    public void onClick(View v)
    {
        switch (v.getId()) {

            case R.id.btn_confirm:
                dismiss();
                break;
            case R.id.btn_cancle:
                dismiss();
                break;

            case R.id.radio_None:
            {
                order_option = "None";
                Report_view.tv_job_status2.setText(order_option);
            }
            break;
            case R.id.radio_Yes:
            {
                order_option = "Yes";
                Report_view.tv_job_status2.setText(order_option);
            }
            break;

            case R.id.radio_No:
            {
                order_option = "No";
                Report_view.tv_job_status2.setText(order_option);
            }
            break;

            default:
                break;
        }

    }

}