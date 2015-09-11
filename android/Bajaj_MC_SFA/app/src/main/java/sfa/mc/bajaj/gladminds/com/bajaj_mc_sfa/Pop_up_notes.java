package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

/**
 * Created by Ranjan on 23-08-2015.
 */



import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.TextView;

public class Pop_up_notes extends Dialog implements android.view.View.OnClickListener
        {
        //	private static final int MODE_PRIVATE = 0;
            Activity context;
            Button btn_cancel, btn_order;
            static String notes="";
            EditText Notes;
        //	private RadioGroup radioOrderGroup;
            boolean get=false;
            String get_text;


//	public Event_mail(Context context, String desc, String title, String strt_time, String nd_time) {
        public Pop_up_notes(Context context) {
            super(context);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.pop_up_notes);
        this.context = (Activity) context;

            Notes = (EditText)findViewById(R.id.edit_notes);
            btn_cancel = (Button)findViewById(R.id.btn_cancle);
            btn_order=(Button)findViewById(R.id.btn_confirm);

            btn_cancel.setOnClickListener(this);
            btn_order.setOnClickListener(this);

/**
            Notes.addTextChangedListener(new TextWatcher() {

                @Override
                public void afterTextChanged(Editable s) {
                    Notes.setText("");
                    get_text=Notes.getText().toString();
                    Report_view.tv_note2.setText(get_text);
                    get=true;
                }

                @Override
                public void beforeTextChanged(CharSequence s, int start,
                                              int count, int after) {
                }

                @Override
                public void onTextChanged(CharSequence s, int start,
                                          int before, int count) {
                    if(s.length() != 0)
                        get_text=Notes.getText().toString();
                        Report_view.tv_note2.setText(get_text);
                        get=true;
                }
            });

 **/

        }


@Override
public void onClick(View v)
        {
        switch (v.getId()) {

        case R.id.btn_confirm:
          /**  if(get=true)
            {
                Report_view.tv_note2.setText(get_text);
            }
**/
            dismiss();

        break;
        case R.id.btn_cancle:
        dismiss();
        break;



        default:
        break;
        }

        }

        }