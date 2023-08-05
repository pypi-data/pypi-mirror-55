#ifndef _PROTON_SRC_SELECTABLE_H
#define _PROTON_SRC_SELECTABLE_H 1

/*
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 */

#ifndef __cplusplus
#include <stdbool.h>
#endif

#include <proton/selectable.h>

void *pni_selectable_get_context(pn_selectable_t *selectable);
void pni_selectable_set_context(pn_selectable_t *selectable, void *context);
int pni_selectable_get_index(pn_selectable_t *selectable);
void pni_selectable_set_index(pn_selectable_t *selectable, int index);

#endif /* selectable.h */
