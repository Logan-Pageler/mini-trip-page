<template>

    <v-table v-if="data!=null && data.length > 0">
        <thead>
        <tr>
            <th v-for="item in data[0]"
            :key="item">
                {{ item }}
            </th>
            <th width="200px"/>
        </tr>
        </thead>
        <tbody>
            <tr
                v-for="i in (data.length - 1)"
                @mouseenter="visible=[];visible[i] = true;"
                @mouseleave="visible[i] = false"
            >
                <td class="text-left"
                v-for="j in data[i].length"
                 >
                    <VTextField
                        v-model="data[i][j - 1]"
                        v-if="editable[i]">
                    </VTextField>
                    <div
                    v-if="!editable[i]">
                        {{ data[i][j - 1] }}
                    </div>
                </td>


                <td>
                    <div v-if="visible[i]">
                        <v-btn
                        variant="outlined"
                        @click="DeleteRow(i);"
                        >
                            <v-icon
                            icon="mdi-delete"
                            />

                        </v-btn>
                        <v-btn
                        variant="outlined"
                        @click="editable[i] = editable[i] ? false : true;print(editable[i])"
                        >
                            <v-icon
                            icon="mdi-pencil"
                            />

                        </v-btn>
                    </div>
                </td>
                   
            </tr>
        </tbody>
    </v-table>
    <div class="py-14" />

    <v-row class="d-flex align-center justify-center">

        <v-col cols="auto">
          <v-btn
            color="primary"
            min-width="228"
            rel="noopener noreferrer"
            size="x-large"
            target="_blank"
            variant="flat"
            id="upload-button"
            @click="Upload();"
          >
            <v-icon
              icon="mdi-tray-arrow-up"
              size="large"
              start
            />

            Upload
          </v-btn>
        </v-col>
        <v-col cols="auto">
          <v-btn
            color="primary"
            min-width="228"
            rel="noopener noreferrer"
            size="x-large"
            target="_blank"
            variant="flat"
            @click="Download();"
          >
            <v-icon
              icon="mdi-download"
              size="large"
              start
            />

            Download
          </v-btn>
        </v-col>

      </v-row>
</template>


<script lang="ts">
import { read, utils, writeFile, WorkBook } from "xlsx"

    export default {
        data() {
            var file : File | null = null as any;
            var data : string[][] = [];
            var wb : WorkBook = null as any;
            var visible : boolean[] = [];
            var editable : boolean[] = [];
            var name : string = null as any;
            return {
                file,
                data,
                wb,
                visible,
                name,
                editable
            };
        },
        methods: {
            Upload() {
                var el = <HTMLInputElement>document.createElement("INPUT");
                el.type = "file";
                el.accept = ".xlsx";
            
                // (cancel will not trigger 'change')
                el.addEventListener('change', (ev2) => {
                    this.file = el.files ? el.files[0] : null;

                    if (this.file) {
                        const reader = new FileReader();

                        reader.onload = (e) => {
                            /* Parse data */
                            const bstr = e.target!.result;
                            this.wb = read(bstr, { type: 'binary' });
                            /* Get first worksheet */
                            this.name = this.wb.SheetNames[0];
                            const ws = this.wb.Sheets[this.name];
                            /* Convert array of arrays */
                            const json : JSON[] = utils.sheet_to_json(ws, { header: 1 });
                            this.data=[];
                            for(let i = 0; i < json.length; i++) {
                                let row : string[] = []
                                for(let j in json[i]) {
                                    row.push(json[i][j]);
                                }
                                this.data.push(row);
                            }
                        }
                        reader.readAsBinaryString(this.file);
                    }
                });

                el.click(); // open
            },
            Download() {
                this.wb.Sheets[this.name] = utils.aoa_to_sheet(this.data);
                writeFile(this.wb, this.name + ".xlsx");
            },
            DeleteRow(row) {
                for(let i = row; i < this.data.length; i++) {
                    this.data[i] = this.data[i+1];
                }
                this.data.pop();
                
                
            },
            print(val) {
                console.log(val);
            }
        }
  
    }
</script>