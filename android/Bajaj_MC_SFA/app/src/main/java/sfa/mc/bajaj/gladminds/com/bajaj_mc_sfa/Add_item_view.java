package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

/**
 * Created by Ranjan on 01-09-2015.
 */
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.view.View;
import android.widget.ImageView;

public class Add_item_view extends FragmentActivity implements View.OnClickListener {

    ImageView imv_back;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.add_item);

        imv_back=(ImageView) findViewById(R.id.iv_back);
        imv_back.setOnClickListener(this);

    }


    @Override
    public void onClick(View v) {

        switch (v.getId()) {


            case R.id.iv_back:{
                finish();
            }
            break;

            case R.id.iv_save:

                break;

            default:
                break;
        }

    }
}
